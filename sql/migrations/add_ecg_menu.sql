SET NAMES utf8mb4;

-- 设置变量存储医疗管理菜单ID
SET @parent_id = (SELECT menu_id FROM sys_menu WHERE menu_name = '医疗管理' LIMIT 1);

-- 添加ECG数据菜单
INSERT INTO sys_menu 
(menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES
('ECG数据', @parent_id, 7, 'ecg', 'medical/ecg/index', 1, 0, 'C', '0', '0', 'medical:ecg:list', 'heartbeat', 'admin', NOW(), 'ECG数据菜单');

-- 设置变量存储ECG菜单ID
SET @ecg_menu_id = (SELECT menu_id FROM sys_menu WHERE menu_name = 'ECG数据' LIMIT 1);

-- 添加ECG数据按钮权限
INSERT INTO sys_menu 
(menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES
('ECG数据查询', @ecg_menu_id, 1, '', '', 1, 0, 'F', '0', '0', 'medical:ecg:query', '#', 'admin', NOW(), ''),
('ECG数据新增', @ecg_menu_id, 2, '', '', 1, 0, 'F', '0', '0', 'medical:ecg:add', '#', 'admin', NOW(), ''),
('ECG数据修改', @ecg_menu_id, 3, '', '', 1, 0, 'F', '0', '0', 'medical:ecg:edit', '#', 'admin', NOW(), ''),
('ECG数据删除', @ecg_menu_id, 4, '', '', 1, 0, 'F', '0', '0', 'medical:ecg:remove', '#', 'admin', NOW(), ''),
('ECG数据导出', @ecg_menu_id, 5, '', '', 1, 0, 'F', '0', '0', 'medical:ecg:export', '#', 'admin', NOW(), ''),
('ECG数据同步', @ecg_menu_id, 6, '', '', 1, 0, 'F', '0', '0', 'medical:ecg:sync', '#', 'admin', NOW(), '');

-- 为管理员角色分配权限
INSERT INTO sys_role_menu(role_id, menu_id)
SELECT 
    (SELECT role_id FROM sys_role WHERE role_key = 'admin' LIMIT 1),
    menu_id
FROM 
    sys_menu 
WHERE 
    menu_name LIKE 'ECG%' 
    AND menu_id NOT IN (SELECT menu_id FROM sys_role_menu WHERE role_id = (SELECT role_id FROM sys_role WHERE role_key = 'admin' LIMIT 1));

-- 确认添加的菜单和权限记录
SELECT 'ECG数据菜单配置已完成' AS result;
SELECT menu_id, menu_name, parent_id, path, perms, icon FROM sys_menu WHERE menu_name LIKE 'ECG%'; 