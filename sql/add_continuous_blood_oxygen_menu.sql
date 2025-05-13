SET NAMES utf8mb4;

-- 添加连续血氧数据菜单
INSERT INTO sys_menu 
(menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
SELECT 
N'连续血氧数据', menu_id, 3, 'continuousBloodOxygen', 'medical/continuousBloodOxygen/index', 1, 0, 'C', '0', '0', 'medical:cbo:list', 'monitor', 'admin', NOW(), N'连续血氧数据菜单'
FROM sys_menu WHERE menu_name = N'医护管理' AND menu_type = 'M';

-- 添加连续血氧数据按钮权限
INSERT INTO sys_menu 
(menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
SELECT 
N'连续血氧查询', menu_id, 1, '', '', 1, 0, 'F', '0', '0', 'medical:cbo:query', '#', 'admin', NOW(), ''
FROM sys_menu WHERE menu_name = N'连续血氧数据' AND menu_type = 'C'
UNION ALL
SELECT 
N'连续血氧新增', menu_id, 2, '', '', 1, 0, 'F', '0', '0', 'medical:cbo:add', '#', 'admin', NOW(), ''
FROM sys_menu WHERE menu_name = N'连续血氧数据' AND menu_type = 'C'
UNION ALL
SELECT 
N'连续血氧修改', menu_id, 3, '', '', 1, 0, 'F', '0', '0', 'medical:cbo:edit', '#', 'admin', NOW(), ''
FROM sys_menu WHERE menu_name = N'连续血氧数据' AND menu_type = 'C'
UNION ALL
SELECT 
N'连续血氧删除', menu_id, 4, '', '', 1, 0, 'F', '0', '0', 'medical:cbo:remove', '#', 'admin', NOW(), ''
FROM sys_menu WHERE menu_name = N'连续血氧数据' AND menu_type = 'C'
UNION ALL
SELECT 
N'连续血氧导出', menu_id, 5, '', '', 1, 0, 'F', '0', '0', 'medical:cbo:export', '#', 'admin', NOW(), ''
FROM sys_menu WHERE menu_name = N'连续血氧数据' AND menu_type = 'C';

-- 为超级管理员角色添加菜单权限
INSERT INTO sys_role_menu(role_id, menu_id)
SELECT 1, menu_id FROM sys_menu WHERE menu_name IN (
    N'连续血氧数据', 
    N'连续血氧查询',
    N'连续血氧新增',
    N'连续血氧修改',
    N'连续血氧删除',
    N'连续血氧导出'
);

-- 为普通角色添加菜单权限（只添加查询权限）
INSERT INTO sys_role_menu(role_id, menu_id)
SELECT 2, menu_id FROM sys_menu WHERE menu_name IN (
    N'连续血氧数据',
    N'连续血氧查询'
);