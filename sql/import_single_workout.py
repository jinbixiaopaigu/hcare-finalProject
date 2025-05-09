#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

def create_table(cursor):
    """创建single_workout_process_detail表"""
    # 先删除已存在的表
    cursor.execute("DROP TABLE IF EXISTS single_workout_process_detail")
    
    sql = """
    CREATE TABLE IF NOT EXISTS single_workout_process_detail (
        id VARCHAR(64) PRIMARY KEY,
        user_id VARCHAR(64),
        record_group_id VARCHAR(64),
        upload_time DATETIME,
        data_time DATETIME,
        activity_name VARCHAR(255),
        activity_type VARCHAR(255),
        activity_intensity VARCHAR(255),
        activity_duration VARCHAR(255),
        activity_duration_unit VARCHAR(32),
        activity_distance FLOAT,
        activity_distance_unit VARCHAR(32),
        activity_calories FLOAT,
        activity_calories_unit VARCHAR(32),
        activity_heart_rate_avg FLOAT,
        activity_heart_rate_avg_unit VARCHAR(32),
        activity_heart_rate_max FLOAT,
        activity_heart_rate_max_unit VARCHAR(32),
        activity_heart_rate_min FLOAT,
        activity_heart_rate_min_unit VARCHAR(32),
        activity_step_count INT,
        activity_step_count_unit VARCHAR(32),
        activity_speed_avg FLOAT,
        activity_speed_avg_unit VARCHAR(32),
        activity_speed_max FLOAT,
        activity_speed_max_unit VARCHAR(32),
        activity_speed_min FLOAT,
        activity_speed_min_unit VARCHAR(32),
        activity_pace_avg FLOAT,
        activity_pace_avg_unit VARCHAR(32),
        activity_pace_max FLOAT,
        activity_pace_max_unit VARCHAR(32),
        activity_pace_min FLOAT,
        activity_pace_min_unit VARCHAR(32),
        activity_altitude_gain FLOAT,
        activity_altitude_gain_unit VARCHAR(32),
        activity_altitude_loss FLOAT,
        activity_altitude_loss_unit VARCHAR(32),
        activity_altitude_max FLOAT,
        activity_altitude_max_unit VARCHAR(32),
        activity_altitude_min FLOAT,
        activity_altitude_min_unit VARCHAR(32),
        external_id VARCHAR(255),
        metadata_version INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
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
            with open('SingleWorkoutProcessDetail.csv', 'r', encoding='utf-8-sig') as f:
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
                        row['活动名称'],
                        None,  # 活动类型(原CSV中没有)
                        row['运动强度'],
                        row['活动.测量时间'] if row['活动.测量时间'].strip() else None,
                        None,  # 活动时长单位(原CSV中没有)
                        float(row['运动距离(m)']) if row['运动距离(m)'].strip() else None,
                        row['运动距离单位'],
                        float(row['卡路里(kcal)']) if row['卡路里(kcal)'].strip() else None,
                        row['卡路里单位'],
                        float(row['心率']) if row['心率'].strip() else None,
                        row['心率单位'],
                        float(row['最大心率']) if row['最大心率'].strip() else None,
                        row['最大心率单位'],
                        float(row['最小心率']) if row['最小心率'].strip() else None,
                        row['最小心率单位'],
                        int(row['步数']) if row['步数'].strip() else None,
                        row['步数单位'],
                        float(row['速度']) if row['速度'].strip() else None,
                        row['速度单位'],
                        None,  # 活动最大速度(原CSV中没有)
                        None,  # 活动最大速度单位(原CSV中没有)
                        None,  # 活动最小速度(原CSV中没有)
                        None,  # 活动最小速度单位(原CSV中没有)
                        None,  # 活动平均配速(原CSV中没有)
                        None,  # 活动平均配速单位(原CSV中没有)
                        None,  # 活动最大配速(原CSV中没有)
                        None,  # 活动最大配速单位(原CSV中没有)
                        None,  # 活动最小配速(原CSV中没有)
                        None,  # 活动最小配速单位(原CSV中没有)
                        None,  # 活动海拔上升(原CSV中没有)
                        None,  # 活动海拔上升单位(原CSV中没有)
                        None,  # 活动海拔下降(原CSV中没有)
                        None,  # 活动海拔下降单位(原CSV中没有)
                        None,  # 活动最高海拔(原CSV中没有)
                        None,  # 活动最高海拔单位(原CSV中没有)
                        None,  # 活动最低海拔(原CSV中没有)
                        None,  # 活动最低海拔单位(原CSV中没有)
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
    INSERT INTO single_workout_process_detail (
        id, user_id, record_group_id, upload_time, data_time,
        activity_name, activity_type, activity_intensity, activity_duration, activity_duration_unit,
        activity_distance, activity_distance_unit, activity_calories, activity_calories_unit,
        activity_heart_rate_avg, activity_heart_rate_avg_unit, activity_heart_rate_max, activity_heart_rate_max_unit,
        activity_heart_rate_min, activity_heart_rate_min_unit, activity_step_count, activity_step_count_unit,
        activity_speed_avg, activity_speed_avg_unit, activity_speed_max, activity_speed_max_unit,
        activity_speed_min, activity_speed_min_unit, activity_pace_avg, activity_pace_avg_unit,
        activity_pace_max, activity_pace_max_unit, activity_pace_min, activity_pace_min_unit,
        activity_altitude_gain, activity_altitude_gain_unit, activity_altitude_loss, activity_altitude_loss_unit,
        activity_altitude_max, activity_altitude_max_unit, activity_altitude_min, activity_altitude_min_unit,
        external_id, metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()
    print("单次运动过程详情数据导入完成")