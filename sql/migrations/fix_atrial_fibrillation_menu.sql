-- 1. 设置菜单可见
UPDATE sys_menu 
SET visible = '0' 
WHERE menu_id = 2010;

-- 2. 为admin角色添加菜单权限
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT role_id, 2010 
FROM sys_role 
WHERE role_key = 'admin';

-- 3. 检查修复结果
SELECT 
    m.menu_id,
    m.menu_name,
    m.visible,
    COUNT(rm.role_id) AS role_count
FROM sys_menu m
LEFT JOIN sys_role_menu rm ON m.menu_id = rm.menu_id
WHERE m.menu_id = 2001
GROUP BY m.menu_id;