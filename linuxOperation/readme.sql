ALTER TABLE `core_mailbox` ADD `last_login` DATETIME NULL DEFAULT NULL COMMENT '最后登录时间' ;
ALTER TABLE `core_mailbox` ADD `is_active` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否是管理员';
ALTER TABLE `core_mailbox` ADD `is_staff` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否是员工';
ALTER TABLE `core_mailbox` ADD `is_superuser` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '超级用户';
ALTER TABLE `core_mailbox` ADD `first_name` VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE `core_mailbox` ADD `last_name` VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
-- ALTER TABLE `core_mailbox` ADD `email` VARCHAR(150) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `last_name`;
ALTER TABLE `core_mailbox` ADD `date_joined` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00';
ALTER TABLE `core_mailbox` ADD `email` VARCHAR(150) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;


ALTER TABLE `co_user` ADD `last_ip` VARCHAR(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '最后登录IP' AFTER `last_login`;

CREATE TABLE `co_user_domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
ALTER TABLE `co_user_domain` ADD UNIQUE( `user_id`, `domain_id`);

CREATE TABLE `co_user_department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `department_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
ALTER TABLE `co_user_department` ADD UNIQUE( `user_id`, `department_id`);


ALTER TABLE `co_department` ADD INDEX(`showorder`);
ALTER TABLE `co_department` ADD INDEX(`parent_id`);
ALTER TABLE `co_department` ADD INDEX(`domain_id`);
ALTER TABLE `oab_share` ADD `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
ALTER TABLE `core_blacklist` ADD `remark` TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注' ;
ALTER TABLE `core_whitelist` ADD `remark` TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注' ;

-- 管理员日志
ALTER TABLE `auditlog_logentry` CHANGE `object_pk` `object_pk` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `object_repr` `object_repr` LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `changes` `changes` LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `remote_addr` `remote_addr` CHAR(39) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `additional_data` `additional_data` LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `extend_type` `extend_type` VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE `auditlog_logentry` CHANGE `extend_content` `extend_content` LONGTEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;





-- 组权限管理
CREATE TABLE `core_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain_id` int(11) NOT NULL DEFAULT '0' COMMENT '所属域名ID',
  `name` varchar(100) CHARACTER SET utf8 NOT NULL COMMENT '组名称',
  `description` text CHARACTER SET utf8 COMMENT '组描述',
  `mail_space` int(11) NOT NULL DEFAULT '0' COMMENT '邮箱空间',
  `net_space` int(11) NOT NULL DEFAULT '0' COMMENT '网络硬盘空间',
  `allow_out_size` int(11) NOT NULL DEFAULT '0' COMMENT '允许外发附件大小',
  `send_limit` tinyint(1) NOT NULL DEFAULT '1' COMMENT '发信功能限制',
  `recv_limit` tinyint(1) NOT NULL DEFAULT '1' COMMENT '收信功能限制',
  `is_limit_send` tinyint(1) NOT NULL DEFAULT '1' COMMENT '限制发送频率',
  `is_pop` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'POP/POPS邮箱收取功能',
  `is_smtp` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'SMTP/SMTPS客户端邮件发送功能',
  `is_imap` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'IMAP/IMAPS客户端邮件收发功能',
  `is_passwd` tinyint(1) NOT NULL DEFAULT '1' COMMENT '定期密码修改设置',
  `passwd_day` int(11) NOT NULL DEFAULT '0' COMMENT '密码有效期',
  `passwd_start` datetime DEFAULT NULL COMMENT '密码有效开始时间',
  `is_passwd_first` tinyint(1) NOT NULL DEFAULT '1' COMMENT '首次登录修改密码',
  `passwd_type` tinyint(1) NOT NULL DEFAULT '2' COMMENT '密码组成字符种类',
  `passwd_other` longtext CHARACTER SET utf8 COMMENT '其他密码规则设置',
  `is_virus` tinyint(1) NOT NULL DEFAULT '1' COMMENT '反病毒功能',
  `is_spam` tinyint(1) NOT NULL DEFAULT '1' COMMENT '反垃圾功能',
  `is_spf` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'SPF检测',
  `is_grey` tinyint(1) NOT NULL DEFAULT '0' COMMENT '灰名单检测',
  `check_attach` longtext CHARACTER SET utf8 COMMENT '检查附件',
  `match_black` longtext CHARACTER SET utf8 COMMENT '匹配黑名单',
  `check_spam` longtext CHARACTER SET utf8 COMMENT '反垃圾引擎',
  `is_formt` tinyint(1) NOT NULL DEFAULT '1' COMMENT '检查发件人格式',
  `spam_folder` varchar(10) CHARACTER SET utf8 NOT NULL DEFAULT 'spam' COMMENT '垃圾邮件投递位置',
  `spam_subject_flag` varchar(200) CHARACTER SET utf8 DEFAULT NULL COMMENT '垃圾邮件主题标识',
  `isolate_day` int(11) NOT NULL DEFAULT '0' COMMENT '隔离邮件保存天数',
  `is_send_isolate` tinyint(1) NOT NULL DEFAULT '0' COMMENT '发送隔离报告',
  `send_isolate_name` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '隔离报告发件人',
  `isolate_url` varchar(200) CHARACTER SET utf8 DEFAULT NULL COMMENT '隔离报告链接地址',
  `check_object` longtext CHARACTER SET utf8 COMMENT '检测对象',
  `check_local` longtext CHARACTER SET utf8 COMMENT '本域进站邮件',
  `check_outside` longtext CHARACTER SET utf8 COMMENT '外域进站邮件',
  `is_info` tinyint(1) NOT NULL DEFAULT '1' COMMENT '个人资料功能',
  `is_passwd_mdf` tinyint(1) NOT NULL DEFAULT '1' COMMENT '密码修改功能',
  `is_param` tinyint(1) NOT NULL DEFAULT '1' COMMENT '参数设置功能',
  `is_signature` tinyint(1) NOT NULL DEFAULT '1' COMMENT '邮件签名功能',
  `is_autoreply` tinyint(1) NOT NULL DEFAULT '1' COMMENT '自动回复功能',
  `is_autotans` tinyint(1) NOT NULL DEFAULT '1' COMMENT '自动转发功能',
  `is_blackwhite` tinyint(1) NOT NULL DEFAULT '1' COMMENT '黑白名单功能',
  `is_tansdefault` tinyint(1) NOT NULL DEFAULT '1' COMMENT '设置自动转发默认值',
  `is_move` tinyint(1) NOT NULL DEFAULT '1' COMMENT '邮箱搬家功能',
  `is_suggest` tinyint(1) NOT NULL DEFAULT '1' COMMENT '邮箱意见反馈功能',
  `is_view` tinyint(1) NOT NULL DEFAULT '1' COMMENT '邮件召回记录查看',
  `is_filter` tinyint(1) NOT NULL DEFAULT '1' COMMENT '邮件过滤功能',
  `is_smtp_tans` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'SMTP外发邮件中转',
  `passwd_level` tinyint(1) NOT NULL DEFAULT '1' COMMENT '账号密级',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
ALTER TABLE `core_group` ADD UNIQUE( `domain_id`, `name`);


CREATE TABLE IF NOT EXISTS `core_group_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `mailbox_id` int(11) NOT NULL,
  `remark` text CHARACTER SET utf8,
  `created` datetime DEFAULT NULL,
   PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
ALTER TABLE `core_group_member` ADD UNIQUE( `group_id`, `mailbox_id`);



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