ALTER TABLE `core_mailbox` ADD `last_login` DATETIME NULL DEFAULT NULL COMMENT '最后登录时间' ;
ALTER TABLE `core_mailbox` ADD `is_active` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否是管理员';
ALTER TABLE `core_mailbox` ADD `is_staff` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否是员工';
ALTER TABLE `core_mailbox` ADD `is_superuser` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '超级用户';
ALTER TABLE `core_mailbox` ADD `first_name` VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE `core_mailbox` ADD `last_name` VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
-- ALTER TABLE `core_mailbox` ADD `email` VARCHAR(150) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `last_name`;
ALTER TABLE `core_mailbox` ADD `date_joined` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00';
ALTER TABLE `core_mailbox` ADD `email` VARCHAR(150) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;


ALTER TABLE `co_department` ADD INDEX(`showorder`);
ALTER TABLE `oab_share` ADD `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
ALTER TABLE `core_blacklist` ADD `remark` TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注' ;
ALTER TABLE `core_whitelist` ADD `remark` TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注' ;

-- 管理员日志
ALTER TABLE `auditlog_logentry` CHANGE `object_pk` `object_pk` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `object_repr` `object_repr` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `changes` `changes` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `remote_addr` `remote_addr` VARCHAR(39) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `additional_data` `additional_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `extend_type` `extend_type` VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `extend_content` `extend_content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL;


-- 组权限管理
CREATE TABLE IF NOT EXISTS `core_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `mail_space` int(11) NOT NULL,
  `net_space` int(11) NOT NULL,
  `allow_out_size` int(11) NOT NULL,
  `send_limit` int(11) NOT NULL,
  `recv_limit` int(11) NOT NULL,
  `is_pop` tinyint(1) NOT NULL,
  `is_smtp` tinyint(1) NOT NULL,
  `is_imap` tinyint(1) NOT NULL,
  `is_passwd` tinyint(1) NOT NULL,
  `passwd_day` int(11) NOT NULL,
  `passwd_start` datetime DEFAULT NULL,
  `is_passwd_first` tinyint(1) NOT NULL,
  `passwd_type` int(11) NOT NULL,
  `passwd_other` longtext,
  `passwd_forbid` longtext,
  `is_virus` tinyint(1) NOT NULL,
  `is_spam` tinyint(1) NOT NULL,
  `is_spf` tinyint(1) NOT NULL,
  `is_grey` tinyint(1) NOT NULL,
  `check_attach` longtext,
  `match_black` longtext,
  `check_spam` longtext,
  `is_formt` tinyint(1) NOT NULL,
  `spam_folder` varchar(10) NOT NULL,
  `spam_subject_flag` varchar(200) DEFAULT NULL,
  `isolate_day` int(11) NOT NULL,
  `is_send_isolate` tinyint(1) NOT NULL,
  `send_isolate_name` varchar(100) DEFAULT NULL,
  `isolate_url` varchar(200) DEFAULT NULL,
  `check_object` longtext,
  `check_local` longtext,
  `check_outside` longtext,
  `is_info` tinyint(1) NOT NULL,
  `is_passwd_mdf` tinyint(1) NOT NULL,
  `is_param` tinyint(1) NOT NULL,
  `is_signature` tinyint(1) NOT NULL,
  `is_autoreply` tinyint(1) NOT NULL,
  `is_autotans` tinyint(1) NOT NULL,
  `is_blackwhite` tinyint(1) NOT NULL,
  `is_tansdefault` tinyint(1) NOT NULL,
  `is_move` tinyint(1) NOT NULL,
  `is_suggest` tinyint(1) NOT NULL,
  `is_view` tinyint(1) NOT NULL,
  `is_filter` tinyint(1) NOT NULL,
  `is_smtp_tans` tinyint(1) NOT NULL,
  `passwd_level` int(11) NOT NULL,
  `is_frequency` tinyint(1) NOT NULL,
  `frequency_minute` int(11) NOT NULL,
  `frequency_minute_count` int(11) NOT NULL,
  `frequency_hour_count` int(11) NOT NULL,
  `frequency_day_count` int(11) NOT NULL,
  `frequency_operate` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_group_domain_id_name_f36fedcc_uniq` (`domain_id`,`name`),
  UNIQUE KEY `domain_id` (`domain_id`,`name`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `core_group_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `mailbox_id` int(11) NOT NULL,
  `remark` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`mailbox_id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

-- 管理员管理
ALTER TABLE `auth_group` CHANGE `name` `name` VARCHAR(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

 CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
ALTER TABLE `auth_user_user_permissions` ADD INDEX(`user_id`);
ALTER TABLE `auth_user_user_permissions` ADD INDEX(`permission_id`);


auth_user_groups | CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
ALTER TABLE `auth_user_groups` ADD INDEX(`user_id`);
ALTER TABLE `auth_user_groups` ADD INDEX(`group_id`);


CREATE TABLE `perm_mypermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL COMMENT '父ID',
  `permission_id` int(11) DEFAULT NULL COMMENT '权限ID',
  `name` varchar(50) NOT NULL COMMENT '权限名称',
  `is_nav` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否为导航',
  `nav_name` varchar(50) NOT NULL COMMENT '导航名称',
  `url` varchar(150) DEFAULT NULL COMMENT '目录url',
  `is_default` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为默认权限',
  `order_id` int(11) NOT NULL DEFAULT '1' COMMENT '导航顺序',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `parent_id` (`parent_id`),
  KEY `permission_id` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
ALTER TABLE `perm_mypermission` ADD INDEX(`url`);
