SET NAMES utf8mb4;

-- 添加医护管理目录
INSERT INTO sys_menu 
(menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES 
(N'医护管理', 0, 4, 'medical', null, 1, 0, 'M', '0', '0', '', 'medical-box', 'admin', NOW(), N'医护管理目录');

-- 添加病人状况菜单
INSERT INTO sys_menu 
(menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
SELECT 
N'病人状况', menu_id, 1, 'patient/condition', 'medical/patient/condition', 1, 0, 'C', '0', '0', 'medical:patient:list', 'user', 'admin', NOW(), N'病人状况菜单'
FROM sys_menu WHERE menu_name = N'医护管理' AND menu_type = 'M';

-- 为超级管理员角色添加菜单权限
INSERT INTO sys_role_menu(role_id, menu_id)
SELECT 1, menu_id FROM sys_menu WHERE menu_name IN (N'医护管理', N'病人状况');

-- 为普通角色添加菜单权限
INSERT INTO sys_role_menu(role_id, menu_id)
SELECT 2, menu_id FROM sys_menu WHERE menu_name IN (N'医护管理', N'病人状况');