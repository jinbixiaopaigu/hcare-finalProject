import csv
import pymysql
from datetime import datetime

def main():
    # 数据库连接配置
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'q1w2e3r4',
        'database': 'hcare-final',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

    # CSV文件路径
    csv_file = 'sql/Acceleration.csv'

    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            # 创建Acceleration表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS Acceleration (
                `数据唯一ID` VARCHAR(36) PRIMARY KEY,
                `用户ID` VARCHAR(36),
                `记录分组ID` VARCHAR(36),
                `上传时间` DATETIME,
                `数据时间` DATETIME,
                `Acceleration` VARCHAR(255),
                `外部ID` VARCHAR(10),
                `元数据版本` INT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            cursor.execute(create_table_sql)
            print("表Acceleration创建成功")

            # 读取并导入CSV数据（明确使用制表符分隔）
            with open(csv_file, 'r', encoding='utf-8') as f:
                # 读取第一行处理BOM头
                first_line = f.readline()
                if first_line.startswith('\ufeff'):
                    first_line = first_line.strip('\ufeff')
                    f.seek(0)
                    f.readline()  # 跳过BOM行
                
                # 重新创建reader，强制使用制表符分隔
                f.seek(0)
                csv_reader = csv.DictReader(f, delimiter='\t')
                
                # 处理列名中的BOM字符
                csv_reader.fieldnames = [name.strip('\ufeff') for name in csv_reader.fieldnames]
                
                # 打印调试信息
                print(f"检测到的分隔符: {repr(delimiter)}")
                print(f"实际列名: {csv_reader.fieldnames}")
                
                # 验证列名
                # 处理带BOM的列名
                fieldnames = [name.strip('\ufeff') for name in csv_reader.fieldnames]
                expected_columns = {
                    '数据唯一ID', '用户ID', '记录分组ID', '上传时间',
                    '数据时间', 'Acceleration', '外部ID', '元数据版本'
                }
                if not expected_columns.issubset(fieldnames):
                    raise ValueError(f"CSV文件缺少必要的列，实际列名: {fieldnames}")
                
                # 创建列名映射
                col_map = {
                    '数据唯一ID': '数据唯一ID',
                    '用户ID': '用户ID',
                    '记录分组ID': '记录分组ID',
                    '上传时间': '上传时间',
                    '数据时间': '数据时间',
                    'Acceleration': 'Acceleration',
                    '外部ID': '外部ID',
                    '元数据版本': '元数据版本'
                }
                
                for row in csv_reader:
                    try:
                        # 准备插入数据
                        insert_sql = """
                        INSERT INTO Acceleration (
                            `数据唯一ID`, `用户ID`, `记录分组ID`, 
                            `上传时间`, `数据时间`, `Acceleration`, 
                            `外部ID`, `元数据版本`
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        # 使用列名映射获取正确的列值
                        try:
                            # 打印调试信息
                            print(f"Processing row {csv_reader.line_num}: {row}")
                            
                            # 确保所有必需字段都存在
                            required_fields = ['数据唯一ID', '用户ID', '记录分组ID', 
                                            '上传时间', '数据时间', 'Acceleration',
                                            '外部ID', '元数据版本']
                            for field in required_fields:
                                if col_map[field] not in row:
                                    raise ValueError(f"Missing required field: {field}")
                            
                            cursor.execute(insert_sql, (
                                row.get(col_map['数据唯一ID'], ''),
                                row.get(col_map['用户ID'], ''),
                                row.get(col_map['记录分组ID'], ''),
                                datetime.strptime(row.get(col_map['上传时间'], '1970-01-01 00:00:00'), '%Y-%m-%d %H:%M:%S'),
                                datetime.strptime(row.get(col_map['数据时间'], '1970-01-01 00:00:00'), '%Y-%m-%d %H:%M:%S'),
                                row.get(col_map['Acceleration'], ''),
                                row.get(col_map['外部ID'], ''),
                                int(row.get(col_map['元数据版本'], 0))
                            ))
                        except Exception as e:
                            print(f"处理行 {csv_reader.line_num} 时出错: {e}")
                            print(f"行数据: {row}")
                            continue
                    except Exception as e:
                        print(f"处理行 {csv_reader.line_num} 时出错: {e}")
                        continue
            
            connection.commit()
            print(f"成功导入{csv_reader.line_num - 1}条数据")

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    main()