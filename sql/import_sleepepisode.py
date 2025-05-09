import csv
import pymysql
from pathlib import Path

# 数据库配置
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'q1w2e3r4',
    'database': 'hcare-final',
    'charset': 'utf8mb4'
}

# CSV文件路径
csv_file = Path(__file__).parent / 'sleepepisode.csv'

def import_data():
    # 连接数据库
    connection = pymysql.connect(**db_config)
    
    try:
        with connection.cursor() as cursor:
            # 读取CSV文件(使用utf-8-sig编码自动去除BOM)
            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                # 打印CSV文件的前几行用于调试
                print("CSV文件前5行内容:")
                for i, line in enumerate(f):
                    if i < 5:
                        print(line.strip())
                    else:
                        break
                f.seek(0)  # 重置文件指针
                
                reader = csv.DictReader(f)
                print("\nCSV文件列名:", reader.fieldnames)

                # 准备批量插入
                batch = []
                for row in reader:
                    batch.append((
                        row['数据唯一ID'],
                        row['用户ID'],
                        row['记录分组ID'] if row['记录分组ID'] else None,
                        row['上传时间'],
                        row['数据时间'],
                        row['入睡开始时间'] if row['入睡开始时间'] else None,
                        row['入睡结束时间'] if row['入睡结束时间'] else None,
                        row['最早入睡时间'] if row['最早入睡时间'] else None,
                        row['出睡开始时间'] if row['出睡开始时间'] else None,
                        row['出睡结束时间'] if row['出睡结束时间'] else None,
                        row['最迟出睡时间'] if row['最迟出睡时间'] else None,
                        row['上床开始时间'] if row['上床开始时间'] else None,
                        row['上床结束时间'] if row['上床结束时间'] else None,
                        row['上床时间'] if row['上床时间'] else None,
                        int(row['睡眠潜伏期']) if row['睡眠潜伏期'].strip() else None,
                        row['睡眠潜伏时长单位'] if row['睡眠潜伏时长单位'].strip() else None,
                        int(row['浅睡时长(min)']) if row['浅睡时长(min)'].strip() else None,
                        row['浅睡时长单位'] if row['浅睡时长单位'].strip() else None,
                        int(row['深睡时长(min)']) if row['深睡时长(min)'].strip() else None,
                        row['深睡时长单位'] if row['深睡时长单位'].strip() else None,
                        int(row['做梦时长(min)']) if row['做梦时长(min)'].strip() else None,
                        row['做梦时长单位'] if row['做梦时长单位'].strip() else None,
                        int(row['清醒时长(min)']) if row['清醒时长(min)'].strip() else None,
                        row['清醒时长单位'] if row['清醒时长单位'].strip() else None,
                        int(row['全部睡眠时长(min)']) if row['全部睡眠时长(min)'].strip() else None,
                        row['全部睡眠时长单位'] if row['全部睡眠时长单位'].strip() else None,
                        int(row['清醒次数']) if row['清醒次数'].strip() else None,
                        int(row['白天睡眠时长']) if row['白天睡眠时长'].strip() else None,
                        row['白天睡眠时长单位'] if row['白天睡眠时长单位'].strip() else None,
                        row['打鼾频率'] if row['打鼾频率'].strip() else None,
                        int(row['睡眠得分']) if row['睡眠得分'].strip() else None,
                        row['用户备注'] if row['用户备注'] else None,
                        row['睡眠详情'],
                        row['外部ID'],
                        row['元数据版本']
                    ))
                    
                    # 每100条执行一次批量插入
                    if len(batch) >= 100:
                        insert_data(cursor, batch)
                        batch = []
                
                # 插入剩余数据
                if batch:
                    insert_data(cursor, batch)
            
            connection.commit()
            print(f"成功导入 {len(batch)} 条数据到 sleepepisode 表")
            
    finally:
        connection.close()

def insert_data(cursor, batch):
    sql = """
    INSERT INTO sleepepisode (
        id, user_id, record_group_id, upload_time, data_time, 
        sleep_start_time, sleep_end_time, earliest_sleep_time,
        wake_start_time, wake_end_time, latest_wake_time,
        bed_start_time, bed_end_time, bed_time,
        sleep_latency, sleep_latency_unit,
        light_sleep_duration, light_sleep_unit,
        deep_sleep_duration, deep_sleep_unit,
        rem_duration, rem_unit,
        awake_duration, awake_unit,
        total_sleep_duration, total_sleep_unit,
        awake_count,
        daytime_sleep_duration, daytime_sleep_unit,
        snoring_frequency, sleep_score, user_notes,
        sleep_details, external_id, metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()