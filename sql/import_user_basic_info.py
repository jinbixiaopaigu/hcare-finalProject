#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

def create_table(cursor):
    """创建UserBasicInfo表"""
    # 先删除已存在的表
    cursor.execute("DROP TABLE IF EXISTS UserBasicInfo")
    
    # 创建新表
    sql = """
    CREATE TABLE UserBasicInfo (
        id VARCHAR(255) PRIMARY KEY,
        user_id VARCHAR(255),
        record_group_id VARCHAR(255),
        upload_time DATETIME,
        data_time DATETIME,
        height FLOAT,
        height_unit VARCHAR(50),
        height_measure_start_time DATETIME,
        height_measure_end_time DATETIME,
        height_measure_time DATETIME,
        height_stat_method VARCHAR(50),
        height_user_notes TEXT,
        weight FLOAT,
        weight_unit VARCHAR(50),
        weight_measure_start_time DATETIME,
        weight_measure_end_time DATETIME,
        weight_measure_time DATETIME,
        weight_stat_method VARCHAR(50),
        weight_user_notes TEXT,
        age INT,
        gender VARCHAR(10),
        province VARCHAR(50),
        city VARCHAR(50),
        register_time DATETIME,
        device_type VARCHAR(255),
        device_version VARCHAR(255),
        app_version VARCHAR(50),
        join_research_time DATETIME,
        phone_type VARCHAR(100),
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
            
            # 读取CSV文件
            with open('sql/UserBasicInfo.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                print("CSV文件列名:", reader.fieldnames)  # 调试输出列名
                batch = []
                
                for row in reader:
                    # 处理数据
                    batch.append((
                        row['数据唯一ID'],
                        row['用户ID'],
                        row['记录分组ID'] if row['记录分组ID'].strip() else None,
                        row['上传时间'],
                        row['数据时间'],
                        float(row['身高(cm)']) if row['身高(cm)'].strip() else None,
                        row['身高单位'] if row['身高单位'].strip() else None,
                        row['身高.测量开始时间'] if row['身高.测量开始时间'].strip() else None,
                        row['身高.测量结束时间'] if row['身高.测量结束时间'].strip() else None,
                        row['身高.测量时间'] if row['身高.测量时间'].strip() else None,
                        row['身高.统计方式'] if row['身高.统计方式'].strip() else None,
                        row['身高.用户备注'] if row['身高.用户备注'].strip() else None,
                        float(row['体重(kg)']) if row['体重(kg)'].strip() else None,
                        row['体重单位'] if row['体重单位'].strip() else None,
                        row['体重.测量开始时间'] if row['体重.测量开始时间'].strip() else None,
                        row['体重.测量结束时间'] if row['体重.测量结束时间'].strip() else None,
                        row['体重.测量时间'] if row['体重.测量时间'].strip() else None,
                        row['体重.统计方式'] if row['体重.统计方式'].strip() else None,
                        row['体重.用户备注'] if row['体重.用户备注'].strip() else None,
                        int(row['年龄']) if row['年龄'].strip() else None,
                        row['性别'] if row['性别'].strip() else None,
                        row['省份'] if row['省份'].strip() else None,
                        row['城市'] if row['城市'].strip() else None,
                        row['注册时间'] if row['注册时间'].strip() else None,
                        row['设备类型'] if row['设备类型'].strip() else None,
                        row['设备版本'] if row['设备版本'].strip() else None,
                        row['APP版本'] if row['APP版本'].strip() else None,
                        row['加入研究项目时间'] if row['加入研究项目时间'].strip() else None,
                        row['手机类型'] if row['手机类型'].strip() else None,
                        row['外部ID'],
                        int(row['元数据版本'])
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
                
    finally:
        connection.close()

def insert_data(cursor, batch):
    sql = """
    INSERT INTO UserBasicInfo (
        id, user_id, record_group_id, upload_time, data_time,
        height, height_unit, height_measure_start_time, height_measure_end_time, 
        height_measure_time, height_stat_method, height_user_notes,
        weight, weight_unit, weight_measure_start_time, weight_measure_end_time,
        weight_measure_time, weight_stat_method, weight_user_notes,
        age, gender, province, city, register_time,
        device_type, device_version, app_version, join_research_time,
        phone_type, external_id, metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()
    print("用户基本信息数据导入完成")