/*
 Navicat Premium Dump SQL

 Source Server         : main
 Source Server Type    : MySQL
 Source Server Version : 80040 (8.0.40)
 Source Host           : localhost:3306
 Source Schema         : hcare-final

 Target Server Type    : MySQL
 Target Server Version : 80040 (8.0.40)
 File Encoding         : 65001

 Date: 10/05/2025 20:28:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for atrial_fibrillation_measure_result
-- ----------------------------
DROP TABLE IF EXISTS `atrial_fibrillation_measure_result`;
CREATE TABLE `atrial_fibrillation_measure_result`  (
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '唯一标识符（32位UUID）',
  `user_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户标识符',
  `group_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '记录分组标识符',
  `upload_time` datetime NOT NULL COMMENT '数据上传时间（服务器时间）',
  `data_time` datetime NOT NULL COMMENT '数据生成时间（设备记录时间）',
  `af_result` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '房颤检测结果（如：normal）',
  `risk_level` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '房颤风险等级（如：normal）',
  `external_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '外部系统关联ID',
  `metadata_version` int NOT NULL DEFAULT 1 COMMENT '元数据版本号',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_group_id`(`group_id` ASC) USING BTREE,
  INDEX `idx_upload_time`(`upload_time` ASC) USING BTREE,
  INDEX `idx_external_id`(`external_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '房颤测量结果记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of atrial_fibrillation_measure_result
-- ----------------------------
INSERT INTO `atrial_fibrillation_measure_result` VALUES ('1b41a8ca05394ebc90a83f26e54b4b5a', '60be804203734c23b883a030fce40dd0', '640452568c894e30b45f863dfe13db3d', '2025-05-02 18:50:32', '2025-05-02 18:50:31', 'normal', 'normal', '1234', 1);

SET FOREIGN_KEY_CHECKS = 1;
