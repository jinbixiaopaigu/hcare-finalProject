#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试MySQL连接的简单程序
"""

import pymysql
import argparse
import traceback

def test_connection(host, port, user, password, db):
    """测试MySQL连接
    
    Args:
        host: 主机名
        port: 端口号
        user: 用户名
        password: 密码
        db: 数据库名
    """
    print(f"正在连接MySQL数据库: {host}:{port}, 用户: {user}, 数据库: {db}")
    if password:
        print(f"使用密码长度: {len(password)}")
    else:
        print("警告：未提供密码")
    
    try:
        # 建立连接
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("连接成功！")
        
        # 测试查询
        with conn.cursor() as cursor:
            # 获取所有表名
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"\n数据库中的表 ({len(tables)}):")
            for i, table in enumerate(tables, 1):
                table_name = list(table.values())[0]
                print(f"{i}. {table_name}")
                
                # 获取表结构
                if i <= 3:  # 仅显示前三个表的结构
                    cursor.execute(f"DESCRIBE `{table_name}`")
                    columns = cursor.fetchall()
                    
                    print(f"   表 {table_name} 的结构:")
                    for col in columns:
                        print(f"   - {col['Field']} ({col['Type']})")
                    print()
        
        # 关闭连接
        conn.close()
        print("\n测试完成，连接已关闭")
        return True
        
    except Exception as e:
        print(f"连接失败: {str(e)}")
        traceback.print_exc()  # 打印完整堆栈跟踪
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='测试MySQL数据库连接')
    parser.add_argument('--host', default='localhost', help='MySQL主机名')
    parser.add_argument('--port', type=int, default=3306, help='MySQL端口号')
    parser.add_argument('--user', default='root', help='MySQL用户名')
    parser.add_argument('--password', default='', help='MySQL密码')
    parser.add_argument('--db', default='hcare-final', help='MySQL数据库名')
    
    args = parser.parse_args()
    
    test_connection(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        db=args.db
    )

if __name__ == "__main__":
    main() 