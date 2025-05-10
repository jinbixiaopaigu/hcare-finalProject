-- 更新血氧饱和度菜单结构

-- 1. 更新主菜单项
UPDATE sys_menu 
SET 
    parent_id = 2000,  -- 医疗管理菜单ID
    path = 'medical/bo',
    order_num = 6,
    update_time = '2025-05-11 01:12:47'  -- 使用sys_menu.sql中的时间格式
WHERE menu_id = 2011;

-- 2. 更新现有按钮权限
UPDATE sys_menu 
SET 
    update_time = '2025-05-11 01:12:47'
WHERE menu_id IN (2012, 2014, 2015, 2016);

-- 3. 添加缺少的按钮权限
INSERT INTO sys_menu VALUES 
(2017, '血氧饱和度导出', 2011, 5, '', '', '', 1, 0, 'F', '0', '0', 'medical:bo:export', '#', 'admin', '2025-05-11 01:12:47', 'admin', '2025-05-11 01:12:47', ''),
(2018, '血氧饱和度导入', 2011, 6, '', '', '', 1, 0, 'F', '0', '0', 'medical:bo:import', '#', 'admin', '2025-05-11 01:12:47', 'admin', '2025-05-11 01:12:47', '');

-- 4. 为管理员角色分配新权限
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT 
    (SELECT role_id FROM sys_role WHERE role_key = 'admin' LIMIT 1),
    menu_id
FROM sys_menu
WHERE menu_id IN (2017, 2018)
AND NOT EXISTS (
    SELECT 1 FROM sys_role_menu 
    WHERE role_id = (SELECT role_id FROM sys_role WHERE role_key = 'admin' LIMIT 1)
    AND menu_id IN (2017, 2018)
);

-- 验证更新
SELECT '血氧饱和度菜单更新完成' AS result;
SELECT menu_id, menu_name, parent_id, path, perms FROM sys_menu WHERE menu_name LIKE '血氧饱和度%';