#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

def create_table(cursor):
    """创建HeartRate表，根据HeartRate.csv的结构"""
    sql = """
    CREATE TABLE IF NOT EXISTS HeartRate (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(36) NOT NULL,
        record_group_id VARCHAR(36),
        upload_time DATETIME NOT NULL,
        data_time DATETIME NOT NULL,
        heart_rate_value INT NOT NULL,
        heart_rate_unit VARCHAR(10) NOT NULL,
        measurement_start_time DATETIME,
        measurement_end_time DATETIME,
        measurement_time DATETIME NOT NULL,
        statistical_description VARCHAR(255),
        body_activity_status VARCHAR(50),
        sleep_status VARCHAR(50),
        user_remark TEXT,
        external_id VARCHAR(36),
        metadata_version INT NOT NULL,
        INDEX idx_user_id (user_id),
        INDEX idx_data_time (data_time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
    cursor.execute(sql)

def import_data():
    """导入HeartRate数据"""
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'q1w2e3r4',
        'database': 'hcare-final',
        'charset': 'utf8mb4'
    }
    
    connection = pymysql.connect(**db_config)
    
    try:
        with connection.cursor() as cursor:
            # 创建表
            create_table(cursor)
            print("表HeartRate创建成功")
            
            # 读取CSV文件
            with open('sql/HeartRate.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                batch = []
                total = 0
                
                for row in reader:
                    # 处理数据
                    batch.append((
                        row['数据唯一ID'],
                        row['用户ID'],
                        row['记录分组ID'] if row['记录分组ID'].strip() else None,
                        row['上传时间'],
                        row['数据时间'],
                        int(row['心率(beats/min)']),
                        row['心率单位'],
                        row['心率.测量开始时间'] if row['心率.测量开始时间'].strip() else None,
                        row['心率.测量结束时间'] if row['心率.测量结束时间'].strip() else None,
                        row['心率.测量时间'],
                        row['心率.统计描述'] if row['心率.统计描述'].strip() else None,
                        row['心率.身体活动状态'] if row['心率.身体活动状态'].strip() else None,
                        row['心率.睡眠状态'] if row['心率.睡眠状态'].strip() else None,
                        row['心率.用户备注'] if row['心率.用户备注'].strip() else None,
                        row['外部ID'] if row['外部ID'].strip() else None,
                        int(row['元数据版本']) if row['元数据版本'].strip() else 0
                    ))
                    
                    # 批量插入
                    if len(batch) >= 100:
                        insert_data(cursor, batch)
                        total += len(batch)
                        print(f"已导入 {total} 条记录", end='\r')
                        batch = []
                
                # 插入剩余数据
                if batch:
                    insert_data(cursor, batch)
                    total += len(batch)
                
                # 提交事务
                connection.commit()
                print(f"\n心率数据导入完成，共导入{total}条记录")
                
    except Exception as e:
        connection.rollback()
        print("\n导入失败:", e)
    finally:
        connection.close()

def insert_data(cursor, batch):
    """批量插入数据"""
    sql = """
    INSERT INTO HeartRate (
        id, user_id, record_group_id, upload_time, data_time,
        heart_rate_value, heart_rate_unit, measurement_start_time,
        measurement_end_time, measurement_time, statistical_description,
        body_activity_status, sleep_status, user_remark, external_id,
        metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s, %s,
        %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()