#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

def create_table(cursor):
    """创建motion表"""
    sql = """
    CREATE TABLE IF NOT EXISTS motion (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(36),
        record_group_id VARCHAR(36),
        upload_time DATETIME,
        data_time DATETIME,
        acceleration VARCHAR(255),
        orientation VARCHAR(255),
        external_id INT,
        metadata_version INT,
        INDEX idx_user_id (user_id),
        INDEX idx_data_time (data_time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
    cursor.execute(sql)

def import_data():
    # 数据库连接配置
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'q1w2e3r4',
        'database': 'hcare-final',
        'charset': 'utf8mb4'
    }
    
    # 连接数据库
    connection = pymysql.connect(**db_config)
    
    try:
        with connection.cursor() as cursor:
            # 创建表
            create_table(cursor)
            
            # 读取CSV文件
            with open('sql/motion.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                batch = []
                
                for row in reader:
                    # 处理数据
                    batch.append((
                        row['数据唯一ID'],
                        row['用户ID'],
                        row['记录分组ID'] if row['记录分组ID'].strip() else None,
                        row['上传时间'],
                        row['数据时间'],
                        row['Acceleration'],
                        row['Orientation'],
                        int(row['外部ID']) if row['外部ID'].strip() else None,
                        int(row['元数据版本']) if row['元数据版本'].strip() else None
                    ))
                    
                    # 批量插入
                    if len(batch) >= 100:
                        insert_data(cursor, batch)
                        batch = []
                
                # 插入剩余数据
                if batch:
                    insert_data(cursor, batch)
                
                # 提交事务
                connection.commit()
                print(f"成功导入 {len(batch)} 条motion数据")
                
    except Exception as e:
        connection.rollback()
        print(f"导入失败: {str(e)}")
    finally:
        connection.close()

def insert_data(cursor, batch):
    sql = """
    INSERT INTO motion (
        id, user_id, record_group_id, upload_time, data_time,
        acceleration, orientation, external_id, metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()
    print("motion数据导入完成")