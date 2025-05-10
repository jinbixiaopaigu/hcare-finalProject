-- 添加房颤检测结果菜单
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (
    '房颤检测结果', 
    (SELECT menu_id FROM sys_menu WHERE menu_name = '医疗管理' LIMIT 1), 
    5, 
    'atrialFibrillation', 
    'medical/atrialFibrillation/index', 
    1, 
    'C', 
    '0', 
    '0', 
    'medical:atrialFibrillation:list', 
    'monitor', 
    'admin', 
    NOW(), 
    'admin', 
    NOW(), 
    '房颤检测结果菜单'
);

-- 添加查询权限
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (
    '房颤检测结果查询', 
    (SELECT menu_id FROM sys_menu WHERE menu_name = '房颤检测结果' LIMIT 1), 
    1, 
    '', 
    '', 
    1, 
    'F', 
    '0', 
    '0', 
    'medical:atrialFibrillation:query', 
    '#', 
    'admin', 
    NOW(), 
    'admin', 
    NOW(), 
    ''
);