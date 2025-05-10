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

def check_menu():
    # 连接数据库
    connection = pymysql.connect(**db_config)
    
    try:
        with connection.cursor() as cursor:
            # 1. 检查房颤检测结果菜单是否存在
            sql = """
            SELECT * FROM sys_menu 
            WHERE menu_name = '房颤检测结果' 
            OR perms = 'medical:atrialFibrillation:list'
            """
            cursor.execute(sql)
            menu = cursor.fetchone()
            
            print("\n1. 菜单项检查结果:")
            pprint(menu)
            
            if not menu:
                print("\n错误: 未找到房颤检测结果菜单")
                return
            
            # 2. 检查菜单是否可见(visible=0表示可见)
            menu_id = menu[0]
            sql = f"SELECT visible FROM sys_menu WHERE menu_id = {menu_id}"
            cursor.execute(sql)
            visible = cursor.fetchone()[0]
            
            print(f"\n2. 菜单可见性: {'可见' if visible == 0 else '不可见'}")
            
            # 3. 检查哪些角色有该菜单权限
            sql = f"""
            SELECT r.role_name, r.role_key 
            FROM sys_role r
            JOIN sys_role_menu rm ON r.role_id = rm.role_id
            WHERE rm.menu_id = {menu_id}
            """
            cursor.execute(sql)
            roles = cursor.fetchall()
            
            print("\n3. 拥有该菜单权限的角色:")
            pprint(roles)
            
            if not roles:
                print("\n警告: 没有任何角色拥有该菜单权限")
            
            # 4. 检查admin角色是否有该菜单
            sql = f"""
            SELECT COUNT(*) 
            FROM sys_role_menu rm
            JOIN sys_role r ON rm.role_id = r.role_id
            WHERE rm.menu_id = {menu_id} AND r.role_key = 'admin'
            """
            cursor.execute(sql)
            admin_has_menu = cursor.fetchone()[0] > 0
            
            print(f"\n4. Admin角色是否有权限: {'是' if admin_has_menu else '否'}")
            
    finally:
        connection.close()

if __name__ == '__main__':
    check_menu()