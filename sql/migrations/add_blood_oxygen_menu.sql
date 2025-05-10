-- 设置变量存储医疗管理菜单ID
SET @parent_id = (SELECT menu_id FROM sys_menu WHERE menu_name = '医疗管理' LIMIT 1);

-- 添加血氧饱和度菜单
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (
    '血氧饱和度', 
    @parent_id, 
    6,  -- 顺序号在房颤检测结果之后
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

-- 设置变量存储血氧饱和度菜单ID
SET @bo_menu_id = (SELECT menu_id FROM sys_menu WHERE menu_name = '血氧饱和度' LIMIT 1);

-- 添加查询权限
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (
    '血氧饱和度查询', 
    @bo_menu_id, 
    1, 
    '', 
    '', 
    1, 
    'F', 
    '0', 
    '0', 
    'medical:bo:query', 
    '#', 
    'admin', 
    NOW(), 
    'admin', 
    NOW(), 
    ''
);

-- 添加新增权限
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (
    '血氧饱和度新增', 
    @bo_menu_id, 
    2, 
    '', 
    '', 
    1, 
    'F', 
    '0', 
    '0', 
    'medical:bo:add', 
    '#', 
    'admin', 
    NOW(), 
    'admin', 
    NOW(), 
    ''
);

-- 添加修改权限
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (
    '血氧饱和度修改', 
    (SELECT menu_id FROM sys_menu WHERE menu_name = '血氧饱和度' LIMIT 1), 
    3, 
    '', 
    '', 
    1, 
    'F', 
    '0', 
    '0', 
    'medical:bo:edit', 
    '#', 
    'admin', 
    NOW(), 
    'admin', 
    NOW(), 
    ''
);

-- 添加删除权限
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (
    '血氧饱和度删除', 
    (SELECT menu_id FROM sys_menu WHERE menu_name = '血氧饱和度' LIMIT 1), 
    4, 
    '', 
    '', 
    1, 
    'F', 
    '0', 
    '0', 
    'medical:bo:remove', 
    '#', 
    'admin', 
    NOW(), 
    'admin', 
    NOW(), 
    ''
);

-- 设置变量存储角色ID和菜单ID
SET @admin_role_id = (SELECT role_id FROM sys_role WHERE role_key = 'admin' LIMIT 1);
SET @bo_menu_id = (SELECT menu_id FROM sys_menu WHERE menu_name = '血氧饱和度' LIMIT 1);

-- 为管理员角色分配血氧饱和度菜单权限
INSERT INTO sys_role_menu (role_id, menu_id)
VALUES (@admin_role_id, @bo_menu_id);

-- 设置变量存储按钮菜单ID
SET @query_id = (SELECT menu_id FROM sys_menu WHERE menu_name = '血氧饱和度查询' LIMIT 1);
SET @add_id = (SELECT menu_id FROM sys_menu WHERE menu_name = '血氧饱和度新增' LIMIT 1);
SET @edit_id = (SELECT menu_id FROM sys_menu WHERE menu_name = '血氧饱和度修改' LIMIT 1);
SET @remove_id = (SELECT menu_id FROM sys_menu WHERE menu_name = '血氧饱和度删除' LIMIT 1);

-- 为管理员角色分配所有血氧饱和度按钮权限
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (@admin_role_id, @query_id);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (@admin_role_id, @add_id);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (@admin_role_id, @edit_id);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (@admin_role_id, @remove_id);