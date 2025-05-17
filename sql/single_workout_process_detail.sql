USE `hcare-final`;

-- 创建6分钟行走测试数据表
CREATE TABLE IF NOT EXISTS `single_workout_process_detail` (
  `id` varchar(36) NOT NULL COMMENT '唯一ID',
  `user_id` varchar(36) NOT NULL COMMENT '用户ID',
  `record_group_id` varchar(36) DEFAULT NULL COMMENT '记录组ID',
  `upload_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
  `data_time` datetime NOT NULL COMMENT '数据记录时间',
  `step_count` int(11) DEFAULT NULL COMMENT '步数',
  `distance` float DEFAULT NULL COMMENT '行走距离',
  `distance_unit` varchar(10) DEFAULT 'm' COMMENT '距离单位',
  `heart_rate` int(11) DEFAULT NULL COMMENT '心率',
  `speed` float DEFAULT NULL COMMENT '速度',
  `speed_unit` varchar(10) DEFAULT 'm/s' COMMENT '速度单位',
  `step_frequency` float DEFAULT NULL COMMENT '步频',
  `calories` float DEFAULT NULL COMMENT '消耗卡路里',
  `workout_type` varchar(50) DEFAULT NULL COMMENT '运动类型',
  `workout_status` varchar(20) DEFAULT NULL COMMENT '运动状态',
  `measurement_start_time` datetime DEFAULT NULL COMMENT '测量开始时间',
  `measurement_end_time` datetime DEFAULT NULL COMMENT '测量结束时间',
  `user_notes` text COMMENT '用户笔记',
  `external_id` varchar(100) DEFAULT NULL COMMENT '外部ID',
  `metadata_version` varchar(20) DEFAULT NULL COMMENT '元数据版本',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_data_time` (`data_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='6分钟行走测试数据表'; 