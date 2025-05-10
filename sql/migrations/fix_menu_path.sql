-- 修复房颤检测结果菜单的path和component
UPDATE sys_menu 
SET 
    path = 'atrialFibrillation',
    component = 'medical/atrialFibrillation/index'
WHERE menu_id = 2010;

-- 验证修复结果
SELECT menu_id, menu_name, path, component 
FROM sys_menu 
WHERE menu_id = 2010;