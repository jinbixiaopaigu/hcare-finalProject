-- Add missing columns to continuous_body_temperature table
ALTER TABLE continuous_body_temperature
ADD COLUMN temperature_value FLOAT,
ADD COLUMN temperature_unit VARCHAR(10) DEFAULT '℃',
ADD COLUMN skin_temperature_value FLOAT,
ADD COLUMN skin_temperature_unit VARCHAR(10),
ADD COLUMN ambient_temperature_value FLOAT,
ADD COLUMN ambient_temperature_unit VARCHAR(10),
ADD COLUMN confidence FLOAT;

-- 如果字段已经存在，则以下语句会失败
-- 可以使用以下方式检查字段是否存在后再添加:
/*
ALTER TABLE continuous_body_temperature 
ADD COLUMN IF NOT EXISTS temperature_value FLOAT COMMENT '体温值';
*/

-- 执行完后，请重新启动应用或刷新数据库连接 