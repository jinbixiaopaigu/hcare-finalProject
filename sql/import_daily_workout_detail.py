#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

def create_table(cursor):
    """创建DailyWorkoutDetail表"""
    sql = """
    CREATE TABLE IF NOT EXISTS daily_workout_detail (
        id VARCHAR(255) PRIMARY KEY,
        user_id VARCHAR(255),
        record_group_id VARCHAR(255),
        upload_time DATETIME,
        data_time DATETIME,
        activity_name TEXT,
        external_id VARCHAR(255),
        metadata_version INT
    )
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
            
            # 读取CSV文件并打印列名
            with open('sql/test.csv', 'r', encoding='utf-8-sig') as f:
                # 先读取第一行获取实际列名
                first_line = f.readline()
                print("CSV文件实际列名:", first_line.strip())
                f.seek(0)  # 重置文件指针
                
                reader = csv.DictReader(f)
                print("DictReader识别的列名:", reader.fieldnames)
                batch = []
                
                for row in reader:
                    # 处理数据
                    batch.append((
                        row['数据唯一ID'],
                        row['用户ID'],
                        row['记录分组ID'] if row['记录分组ID'].strip() else None,
                        row['上传时间'],
                        row['数据时间'],
                        row['活动名称'],
                        row['外部ID'],
                        int(row['元数据版本']) if row['元数据版本'].strip() else 1
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
                
    except Exception as e:
        print(f"导入数据时出错: {e}")
        connection.rollback()
    finally:
        connection.close()

def insert_data(cursor, batch):
    sql = """
    INSERT INTO daily_workout_detail (
        id, user_id, record_group_id, upload_time, data_time,
        activity_name, external_id, metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()
    print("日常运动数据导入完成")