-- 解决方案1：先查询出父菜单ID再插入
SET @parent_id = (SELECT menu_id FROM sys_menu WHERE menu_name = '医疗管理' LIMIT 1);

-- 添加房颤检测结果菜单
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (
    '房颤检测结果', 
    @parent_id, 
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

-- 解决方案2：使用临时表方式
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
SELECT 
    '房颤检测结果', 
    menu_id, 
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
FROM sys_menu 
WHERE menu_name = '医疗管理' 
LIMIT 1;