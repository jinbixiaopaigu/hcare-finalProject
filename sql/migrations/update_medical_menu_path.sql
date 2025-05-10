SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
-- 更新房颤检测菜单路径
UPDATE sys_menu 
SET 
    path = 'medical/af',
    perms = 'medical:af:list'
WHERE menu_name = '房颤检测结果';

-- 更新权限标识
UPDATE sys_menu 
SET 
    perms = 'medical:af:query'
WHERE menu_name = '房颤检测结果查询';

-- 验证更新
SELECT menu_id, menu_name, path, component, perms 
FROM sys_menu 
WHERE path LIKE '%medical%';