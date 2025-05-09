#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

def create_table(cursor):
    """创建ContinuousRRI表"""
    sql = """
    CREATE TABLE IF NOT EXISTS ContinuousRRI (
        id VARCHAR(64) PRIMARY KEY,
        user_id VARCHAR(64) NOT NULL,
        record_group_id VARCHAR(64),
        upload_time DATETIME NOT NULL,
        data_time DATETIME NOT NULL,
        rri_data JSON NOT NULL,
        external_id VARCHAR(64),
        metadata_version INT NOT NULL,
        INDEX idx_user_id (user_id),
        INDEX idx_data_time (data_time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
    cursor.execute(sql)

def import_data():
    """导入ContinuousRRI数据"""
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
            
            with open('sql/ContinuousRRI.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                batch = []
                
                for i, row in enumerate(reader):
                    
                    # 处理数据
                    batch.append((
                        row['数据唯一ID'],
                        row['用户ID'],
                        row['记录分组ID'] if row['记录分组ID'].strip() else None,
                        row['上传时间'],
                        row['数据时间'],
                        row['RRI数据'],
                        row['外部ID'] if row['外部ID'].strip() else None,
                        int(row['元数据版本']) if row['元数据版本'].strip() else 0
                    ))
                
                # 插入数据
                if batch:
                    insert_data(cursor, batch)
                
                # 提交事务
                connection.commit()
                print("ContinuousRRI数据导入完成，共导入{}条记录".format(len(batch)))
                
    except Exception as e:
        connection.rollback()
        print("导入失败:", e)
    finally:
        connection.close()

def insert_data(cursor, batch):
    """批量插入数据"""
    sql = """
    INSERT INTO ContinuousRRI (
        id, user_id, record_group_id, upload_time, data_time,
        rri_data, external_id, metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()