USE `hcare-final`;

-- 添加6分钟行走测试数据菜单
INSERT INTO `sys_menu` (`menu_id`, `menu_name`, `parent_id`, `order_num`, `path`, `component`, `query`, `is_frame`, `is_cache`, `menu_type`, `visible`, `status`, `perms`, `icon`, `create_by`, `create_time`, `update_by`, `update_time`, `remark`) 
VALUES 
(3000, '6分钟行走测试', 2000, 6, 'singleWorkoutDetail', 'medical/singleWorkoutDetail/index', NULL, 1, 0, 'C', '0', '0', 'medical:singleWorkoutDetail:list', 'guide', 'admin', NOW(), '', NULL, '6分钟行走测试数据菜单');

-- 添加6分钟行走测试数据按钮权限
INSERT INTO `sys_menu` (`menu_id`, `menu_name`, `parent_id`, `order_num`, `path`, `component`, `query`, `is_frame`, `is_cache`, `menu_type`, `visible`, `status`, `perms`, `icon`, `create_by`, `create_time`, `update_by`, `update_time`, `remark`) 
VALUES 
(3001, '6分钟行走测试查询', 3000, 1, '#', '', NULL, 1, 0, 'F', '0', '0', 'medical:singleWorkoutDetail:query', '#', 'admin', NOW(), '', NULL, ''),
(3002, '6分钟行走测试新增', 3000, 2, '#', '', NULL, 1, 0, 'F', '0', '0', 'medical:singleWorkoutDetail:add', '#', 'admin', NOW(), '', NULL, ''),
(3003, '6分钟行走测试修改', 3000, 3, '#', '', NULL, 1, 0, 'F', '0', '0', 'medical:singleWorkoutDetail:edit', '#', 'admin', NOW(), '', NULL, ''),
(3004, '6分钟行走测试删除', 3000, 4, '#', '', NULL, 1, 0, 'F', '0', '0', 'medical:singleWorkoutDetail:remove', '#', 'admin', NOW(), '', NULL, ''),
(3005, '6分钟行走测试同步', 3000, 5, '#', '', NULL, 1, 0, 'F', '0', '0', 'medical:singleWorkoutDetail:sync', '#', 'admin', NOW(), '', NULL, '');

-- 添加角色-菜单关联
INSERT INTO `sys_role_menu` (`role_id`, `menu_id`) 
SELECT 1, `menu_id` 
FROM `sys_menu` 
WHERE `menu_id` BETWEEN 3000 AND 3005; 