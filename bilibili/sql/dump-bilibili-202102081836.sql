create database bilibili;

--
-- Table structure for table `up_info`
--

DROP TABLE IF EXISTS `up_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `up_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `mid` bigint(20) NOT NULL COMMENT 'mid',
  `name` varchar(255) DEFAULT NULL COMMENT '昵称',
  `url` varchar(255) DEFAULT NULL COMMENT '个人主页url',
  `live_url` varchar(255) DEFAULT NULL COMMENT '直播间url',
  `fssl` int(10) DEFAULT NULL,
  `spsl` int(10) DEFAULT NULL,
  `ydl` int(10) DEFAULT NULL,
  `dzl` int(10) DEFAULT NULL,
  `bfl` int(10) DEFAULT NULL,
  `yn` tinyint(4) DEFAULT '1' COMMENT '是否生效',
  `created` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modified` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COMMENT='up info';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `video`
--

DROP TABLE IF EXISTS `video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `up_name` varchar(100) DEFAULT NULL,
  `mid` bigint(20) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL COMMENT 'url',
  `bfl` int(10) DEFAULT NULL,
  `plsl` int(10) DEFAULT NULL,
  `dt` varchar(255) DEFAULT NULL,
  `length` varchar(255) DEFAULT NULL,
  `dmsl` int(10) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `comments` text,
  `yn` tinyint(4) DEFAULT '1' COMMENT '是否生效',
  `created` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modified` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=854 DEFAULT CHARSET=utf8mb4 COMMENT='up info';