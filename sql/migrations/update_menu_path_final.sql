-- 更新房颤检测结果菜单的path
UPDATE sys_menu 
SET path = 'medical/atrialFibrillation'
WHERE menu_id = 2010;

-- 验证更新
SELECT menu_id, menu_name, path, component 
FROM sys_menu 
WHERE menu_id = 2010;