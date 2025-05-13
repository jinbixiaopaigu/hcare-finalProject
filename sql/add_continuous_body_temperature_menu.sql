-- 添加持续体温数据菜单项
-- 1. 首先查询医疗菜单的父ID
SET @parentId = (SELECT menu_id FROM sys_menu WHERE menu_name = '医疗数据' AND parent_id = 0);

-- 2. 添加主菜单项
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('持续体温数据', @parentId, 6, 'continuousBodyTemperature', 'medical/continuousBodyTemperature/index', 1, 'C', '0', '0', 'medical:continuousBodyTemperature:list', 'monitor', 'admin', sysdate(), '', null, '持续体温数据菜单');

-- 获取刚插入的菜单ID
SET @menuId = LAST_INSERT_ID();

-- 3. 添加子菜单项
-- 查询
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('持续体温查询', @menuId, 1, '', '', 1, 'F', '0', '0', 'medical:continuousBodyTemperature:query', '#', 'admin', sysdate(), '', null, '');

-- 新增
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('持续体温新增', @menuId, 2, '', '', 1, 'F', '0', '0', 'medical:continuousBodyTemperature:add', '#', 'admin', sysdate(), '', null, '');

-- 修改
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('持续体温修改', @menuId, 3, '', '', 1, 'F', '0', '0', 'medical:continuousBodyTemperature:edit', '#', 'admin', sysdate(), '', null, '');

-- 删除
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('持续体温删除', @menuId, 4, '', '', 1, 'F', '0', '0', 'medical:continuousBodyTemperature:remove', '#', 'admin', sysdate(), '', null, '');

-- 导出
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('持续体温导出', @menuId, 5, '', '', 1, 'F', '0', '0', 'medical:continuousBodyTemperature:export', '#', 'admin', sysdate(), '', null, '');

-- 4. 为admin角色添加菜单权限
-- 获取admin角色ID
SET @roleId = (SELECT role_id FROM sys_role WHERE role_key = 'admin');

-- 为admin角色添加所有新菜单项的权限
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (@roleId, @menuId);
INSERT INTO sys_role_menu (role_id, menu_id) SELECT @roleId, menu_id FROM sys_menu WHERE parent_id = @menuId;

COMMIT;
SELECT '持续体温数据菜单添加完成' AS '结果';