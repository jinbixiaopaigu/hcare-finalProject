#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

def create_table(cursor):
    """创建dailyworkout表，根据dailyworkout.csv的结构"""
    # 先删除已存在的表
    cursor.execute("DROP TABLE IF EXISTS dailyworkout")
    
    sql = """
    CREATE TABLE IF NOT EXISTS dailyworkout (
        id VARCHAR(191) PRIMARY KEY,
        user_id VARCHAR(36) NOT NULL,
        record_group_id VARCHAR(36),
        upload_time DATETIME NOT NULL,
        data_time DATETIME NOT NULL,
        activity_name VARCHAR(255) NOT NULL,
        activity_type VARCHAR(100),
        activity_duration INT,
        duration_unit VARCHAR(20),
        distance DECIMAL(10,2),
        distance_unit VARCHAR(20),
        calories DECIMAL(10,2),
        calories_unit VARCHAR(20),
        steps INT,
        steps_unit VARCHAR(20),
        speed DECIMAL(10,2),
        speed_unit VARCHAR(20),
        elevation_gain DECIMAL(10,2),
        elevation_gain_unit VARCHAR(20),
        elevation_loss DECIMAL(10,2),
        elevation_loss_unit VARCHAR(20),
        heart_rate_avg INT,
        heart_rate_avg_unit VARCHAR(20),
        heart_rate_max INT,
        heart_rate_max_unit VARCHAR(20),
        heart_rate_min INT,
        heart_rate_min_unit VARCHAR(20),
        user_remark TEXT,
        external_id VARCHAR(36),
        metadata_version INT NOT NULL,
        INDEX idx_user_id (user_id),
        INDEX idx_data_time (data_time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
    cursor.execute(sql)

def import_data():
    """导入dailyworkout数据"""
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
            print("表dailyworkout创建成功")
            
            # 读取CSV文件
            with open('sql/dailyworkout.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                batch = []
                total = 0
                
                for row in reader:
                    # 处理数据
                    batch.append((
                        row['数据唯一ID'][:190],  # 截断超过191字符的ID
                        row['用户ID'],
                        row['记录分组ID'] if '记录分组ID' in row and row['记录分组ID'].strip() else None,
                        row['上传时间'],
                        row['数据时间'],
                        row['活动名称'],
                        None,  # activity_type (原活动类型)
                        int(row['运动总时长']) if '运动总时长' in row and row['运动总时长'].strip() else None,
                        row['运动总时长单位'] if '运动总时长单位' in row and row['运动总时长单位'].strip() else None,
                        float(row['运动距离(m)']) if '运动距离(m)' in row and row['运动距离(m)'].strip() else None,
                        row['运动距离单位'] if '运动距离单位' in row and row['运动距离单位'].strip() else None,
                        float(row['卡路里']) if '卡路里' in row and row['卡路里'].strip() else None,
                        row['卡路里单位'] if '卡路里单位' in row and row['卡路里单位'].strip() else None,
                        int(row['步数(steps)']) if '步数(steps)' in row and row['步数(steps)'].strip() else None,
                        row['步数单位'] if '步数单位' in row and row['步数单位'].strip() else None,
                        float(row['速度']) if '速度' in row and row['速度'].strip() else None,
                        row['速度单位'] if '速度单位' in row and row['速度单位'].strip() else None,
                        float(row['累计爬升高度']) if '累计爬升高度' in row and row['累计爬升高度'].strip() else None,
                        row['累计爬升高度单位'] if '累计爬升高度单位' in row and row['累计爬升高度单位'].strip() else None,
                        None,  # elevation_loss
                        None,  # elevation_loss_unit
                        int(row['心率']) if '心率' in row and row['心率'].strip() else None,
                        row['心率单位'] if '心率单位' in row and row['心率单位'].strip() else None,
                        int(row['最大心率']) if '最大心率' in row and row['最大心率'].strip() else None,
                        row['最大心率单位'] if '最大心率单位' in row and row['最大心率单位'].strip() else None,
                        int(row['最小心率']) if '最小心率' in row and row['最小心率'].strip() else None,
                        row['最小心率单位'] if '最小心率单位' in row and row['最小心率单位'].strip() else None,
                        row['用户备注'] if '用户备注' in row and row['用户备注'].strip() else None,
                        row['外部ID'] if '外部ID' in row and row['外部ID'].strip() else None,
                        int(row['元数据版本']) if '元数据版本' in row and row['元数据版本'].strip() else 0
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
                print(f"\n每日运动数据导入完成，共导入{total}条记录")
                
    except Exception as e:
        connection.rollback()
        print("\n导入失败:", e)
    finally:
        connection.close()

def insert_data(cursor, batch):
    """批量插入数据"""
    sql = """
    INSERT INTO dailyworkout (
        id, user_id, record_group_id, upload_time, data_time,
        activity_name, activity_type, activity_duration, duration_unit,
        distance, distance_unit, calories, calories_unit,
        steps, steps_unit, speed, speed_unit,
        elevation_gain, elevation_gain_unit, elevation_loss, elevation_loss_unit,
        heart_rate_avg, heart_rate_avg_unit, heart_rate_max, heart_rate_max_unit,
        heart_rate_min, heart_rate_min_unit, user_remark, external_id,
        metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()