import pymysql
from pprint import pprint

# 数据库配置
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'q1w2e3r4',
    'database': 'hcare-final',
    'charset': 'utf8mb4'
}

def check_menu_path():
    # 连接数据库
    connection = pymysql.connect(**db_config)
    
    try:
        with connection.cursor() as cursor:
            # 查询房颤检测结果菜单的path配置
            sql = """
            SELECT menu_id, menu_name, path, component 
            FROM sys_menu 
            WHERE menu_name = '房颤检测结果'
            """
            cursor.execute(sql)
            menu = cursor.fetchone()
            
            print("菜单path配置检查结果:")
            pprint(menu)
            
    finally:
        connection.close()

if __name__ == '__main__':
    check_menu_path()