USE `hcare-final`;

-- 添加连续RRI数据菜单
INSERT INTO `sys_menu` (`menu_id`, `menu_name`, `parent_id`, `order_num`, `path`, `component`, `query`, `is_frame`, `is_cache`, `menu_type`, `visible`, `status`, `perms`, `icon`, `create_by`, `create_time`, `update_by`, `update_time`, `remark`) 
VALUES 
(2015, '连续RRI数据', 2000, 5, 'continuousRRI', 'medical/continuousRRI/index', NULL, 1, 0, 'C', '0', '0', 'medical:continuousRRI:list', 'chart', 'admin', NOW(), '', NULL, '连续RRI数据菜单');

-- 添加连续RRI数据按钮权限
INSERT INTO `sys_menu` (`menu_id`, `menu_name`, `parent_id`, `order_num`, `path`, `component`, `query`, `is_frame`, `is_cache`, `menu_type`, `visible`, `status`, `perms`, `icon`, `create_by`, `create_time`, `update_by`, `update_time`, `remark`) 
VALUES 
(2016, '连续RRI数据查询', 2015, 1, '#', '', NULL, 1, 0, 'F', '0', '0', 'medical:continuousRRI:query', '#', 'admin', NOW(), '', NULL, ''),
(2017, '连续RRI数据新增', 2015, 2, '#', '', NULL, 1, 0, 'F', '0', '0', 'medical:continuousRRI:add', '#', 'admin', NOW(), '', NULL, ''),
(2018, '连续RRI数据修改', 2015, 3, '#', '', NULL, 1, 0, 'F', '0', '0', 'medical:continuousRRI:edit', '#', 'admin', NOW(), '', NULL, ''),
(2019, '连续RRI数据删除', 2015, 4, '#', '', NULL, 1, 0, 'F', '0', '0', 'medical:continuousRRI:remove', '#', 'admin', NOW(), '', NULL, ''),
(2020, '连续RRI数据同步', 2015, 5, '#', '', NULL, 1, 0, 'F', '0', '0', 'medical:continuousRRI:sync', '#', 'admin', NOW(), '', NULL, '');

-- 添加角色-菜单关联
INSERT INTO `sys_role_menu` (`role_id`, `menu_id`) 
SELECT 1, `menu_id` 
FROM `sys_menu` 
WHERE `menu_id` BETWEEN 2015 AND 2020; 