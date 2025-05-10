-- 血氧饱和度菜单SQL脚本(最终版)
-- 使用变量避免子查询，解决1093错误

-- 1. 查询并存储所有需要的ID
SET @parent_id = (SELECT menu_id FROM sys_menu WHERE menu_name = '医疗管理' LIMIT 1);
SET @admin_role_id = (SELECT role_id FROM sys_role WHERE role_key = 'admin' LIMIT 1);

-- 2. 添加血氧饱和度主菜单
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (
    '血氧饱和度', 
    @parent_id, 
    6,
    'bloodOxygen', 
    'medical/bloodOxygen/index', 
    1, 
    'C', 
    '0', 
    '0', 
    'medical:bo:list', 
    'eye-open', 
    'admin', 
    NOW(), 
    'admin', 
    NOW(), 
    '血氧饱和度菜单'
);

-- 3. 获取主菜单ID
SET @bo_menu_id = LAST_INSERT_ID();

-- 4. 添加按钮权限
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES 
('血氧饱和度查询', @bo_menu_id, 1, '', '', 1, 'F', '0', '0', 'medical:bo:query', '#', 'admin', NOW(), 'admin', NOW(), ''),
('血氧饱和度新增', @bo_menu_id, 2, '', '', 1, 'F', '0', '0', 'medical:bo:add', '#', 'admin', NOW(), 'admin', NOW(), ''),
('血氧饱和度修改', @bo_menu_id, 3, '', '', 1, 'F', '0', '0', 'medical:bo:edit', '#', 'admin', NOW(), 'admin', NOW(), ''),
('血氧饱和度删除', @bo_menu_id, 4, '', '', 1, 'F', '0', '0', 'medical:bo:remove', '#', 'admin', NOW(), 'admin', NOW(), '');

-- 5. 为管理员角色分配权限
INSERT INTO sys_role_menu (role_id, menu_id)
VALUES 
(@admin_role_id, @bo_menu_id),
(@admin_role_id, (SELECT menu_id FROM sys_menu WHERE parent_id = @bo_menu_id AND perms = 'medical:bo:query' LIMIT 1)),
(@admin_role_id, (SELECT menu_id FROM sys_menu WHERE parent_id = @bo_menu_id AND perms = 'medical:bo:add' LIMIT 1)),
(@admin_role_id, (SELECT menu_id FROM sys_menu WHERE parent_id = @bo_menu_id AND perms = 'medical:bo:edit' LIMIT 1)),
(@admin_role_id, (SELECT menu_id FROM sys_menu WHERE parent_id = @bo_menu_id AND perms = 'medical:bo:remove' LIMIT 1));

-- 6. 验证语句(可选)
SELECT '血氧饱和度菜单添加完成' AS result;
SELECT COUNT(*) AS menu_count FROM sys_menu WHERE menu_name LIKE '血氧饱和度%';
SELECT COUNT(*) AS role_menu_count FROM sys_role_menu WHERE menu_id = @bo_menu_id;