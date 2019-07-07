-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: localhost    Database: master_manager
-- ------------------------------------------------------
-- Server version	5.7.24-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `orders_weibo_comment`
--

DROP TABLE IF EXISTS `orders_weibo_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders_weibo_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(20) NOT NULL COMMENT '订单号',
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_name` varchar(45) DEFAULT NULL COMMENT '此刻微博评论产品的名称',
  `product_types` tinyint(1) DEFAULT NULL COMMENT '此刻微博评论产品的类型',
  `product_numbers` int(11) DEFAULT NULL COMMENT '总共需要完成的评论的数量',
  `product_nombers_done` int(11) DEFAULT NULL COMMENT '已完成评论的数量',
  `product_price` decimal(10,0) DEFAULT NULL COMMENT '此刻微博评论产品的价格',
  `weibo_url` varchar(200) NOT NULL,
  `comments` text COMMENT '备注',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `status` tinyint(1) DEFAULT '0' COMMENT '0：新建；1：已完成；2：已取消；3：处理中',
  PRIMARY KEY (`id`),
  KEY `orders_weibo_comment_user_id_index` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微博评论订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_weibo_comment`
--

LOCK TABLES `orders_weibo_comment` WRITE;
/*!40000 ALTER TABLE `orders_weibo_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_weibo_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_weibo_comment_like`
--

DROP TABLE IF EXISTS `orders_weibo_comment_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders_weibo_comment_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(20) NOT NULL COMMENT '订单号',
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_name` varchar(45) DEFAULT NULL COMMENT '此刻微博评论点赞产品的名称',
  `product_types` tinyint(1) DEFAULT NULL COMMENT '此刻微博评论点赞产品的类型',
  `product_numbers` int(11) DEFAULT NULL COMMENT '总共需要完成的微博评论点赞的数量',
  `product_nombers_done` int(11) DEFAULT NULL COMMENT '已完成微博评论点赞的数量',
  `product_price` decimal(10,0) DEFAULT NULL COMMENT '此刻微博评论点赞产品的价格',
  `weibo_url` varchar(200) NOT NULL COMMENT '微博评论url',
  `comment_id` varchar(20) NOT NULL COMMENT '评论id',
  `comments` text COMMENT '备注',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `status` tinyint(1) DEFAULT '0' COMMENT '0：新建；1：已完成；2：已取消；3：处理中',
  PRIMARY KEY (`id`),
  KEY `orders_weibo_comment_like_user_id_index` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微博评论点赞订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_weibo_comment_like`
--

LOCK TABLES `orders_weibo_comment_like` WRITE;
/*!40000 ALTER TABLE `orders_weibo_comment_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_weibo_comment_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_weibo_follow`
--

DROP TABLE IF EXISTS `orders_weibo_follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders_weibo_follow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(20) NOT NULL COMMENT '订单号',
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_name` varchar(45) DEFAULT NULL COMMENT '此刻微博关注产品的名称',
  `product_types` tinyint(1) DEFAULT NULL COMMENT '此刻微博关注产品的类型',
  `product_numbers` int(11) DEFAULT NULL COMMENT '总共需要完成的关注的数量',
  `product_nombers_done` int(11) DEFAULT NULL COMMENT '已完成关注的数量',
  `product_price` decimal(10,0) DEFAULT NULL COMMENT '此刻微博关注产品的价格',
  `weibo_url` varchar(200) NOT NULL,
  `comments` text COMMENT '备注',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `status` tinyint(1) DEFAULT '0' COMMENT '0：新建；1：已完成；2：已取消；3：处理中',
  PRIMARY KEY (`id`),
  KEY `orders_weibo_follow_user_id_index` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微博关注订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_weibo_follow`
--

LOCK TABLES `orders_weibo_follow` WRITE;
/*!40000 ALTER TABLE `orders_weibo_follow` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_weibo_follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_weibo_forward`
--

DROP TABLE IF EXISTS `orders_weibo_forward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders_weibo_forward` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(20) NOT NULL COMMENT '订单号',
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_name` varchar(45) DEFAULT NULL COMMENT '此刻微博转发产品的名称',
  `product_types` tinyint(1) DEFAULT NULL COMMENT '此刻微博转发产品的类型',
  `product_numbers` int(11) DEFAULT NULL COMMENT '总共需要完成的转发的数量',
  `product_nombers_done` int(11) DEFAULT NULL COMMENT '已完成转发的数量',
  `product_price` decimal(10,0) DEFAULT NULL COMMENT '此刻微博转发产品的价格',
  `weibo_url` varchar(200) NOT NULL,
  `comments` text COMMENT '备注',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `status` tinyint(1) DEFAULT '0' COMMENT '0：新建；1：已完成；2：已取消；3：处理中',
  PRIMARY KEY (`id`),
  KEY `orders_weibo_forward_user_id_index` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微博转发订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_weibo_forward`
--

LOCK TABLES `orders_weibo_forward` WRITE;
/*!40000 ALTER TABLE `orders_weibo_forward` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_weibo_forward` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_weibo_like`
--

DROP TABLE IF EXISTS `orders_weibo_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders_weibo_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(20) NOT NULL COMMENT '订单号',
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_name` varchar(45) DEFAULT NULL COMMENT '此刻微博点赞产品的名称',
  `product_types` tinyint(1) DEFAULT NULL COMMENT '此刻微博点赞产品的类型',
  `product_numbers` int(11) DEFAULT NULL COMMENT '总共需要完成的点赞的数量',
  `product_nombers_done` int(11) DEFAULT NULL COMMENT '已完成点赞的数量',
  `product_price` decimal(10,0) DEFAULT NULL COMMENT '此刻微博点赞产品的价格',
  `weibo_url` varchar(200) NOT NULL,
  `comments` text COMMENT '备注',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `status` tinyint(1) DEFAULT '0' COMMENT '0：新建；1：已完成；2：已取消；3：处理中',
  PRIMARY KEY (`id`),
  KEY `orders_weibo_like_user_id_index` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COMMENT='微博点赞订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_weibo_like`
--

LOCK TABLES `orders_weibo_like` WRITE;
/*!40000 ALTER TABLE `orders_weibo_like` DISABLE KEYS */;
INSERT INTO `orders_weibo_like` VALUES (1,'1553236413832816',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6905033106/HkTh059g2?from=page_1005056905033106_profile&wvr=6&mod=weibotime','ces','2019-03-22 06:33:34',NULL,1),(2,'1553759179779996',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn0JQEpFw?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment','docker test','2019-03-28 07:46:20',NULL,0),(3,'1553759522040840',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn0JQEpFw?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment','docker test','2019-03-28 07:52:02',NULL,0),(4,'1553761566476521',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn0JQEpFw?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment','docker test','2019-03-28 08:26:06',NULL,0),(5,'1553761674004093',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn0JQEpFw?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment','docker test','2019-03-28 08:27:54',NULL,0),(6,'1553761796301147',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn0JQEpFw?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment','docker test','2019-03-28 08:29:56',NULL,0),(7,'1553763609006085',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn0JQEpFw?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment','docker test2','2019-03-28 09:00:09',NULL,1),(8,'1553828221834103',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/1788911247/Hn8gGD04w?ref=home&rid=0_0_8_4727666396166226769_0_0_0&type=comment#_rnd1553828211231','test','2019-03-29 02:57:02',NULL,0),(9,'1553828343535539',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/1788911247/Hn8gGD04w?ref=home&rid=0_0_8_4727666396166226769_0_0_0&type=comment#_rnd1553828211231','test','2019-03-29 02:59:04',NULL,1),(10,'1553828443992037',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn8itqgx0?from=page_1005056489202878_profile&wvr=6&mod=weibotime','test','2019-03-29 03:00:44',NULL,0),(11,'1553828771054229',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn8itqgx0?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment','test','2019-03-29 03:06:11',NULL,1),(12,'1553829732145966',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn8itqgx0?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment','test','2019-03-29 03:22:12',NULL,0),(13,'1553829838682740',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn8itqgx0?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment','test','2019-03-29 03:23:59',NULL,0),(14,'1553830001890841',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn8itqgx0?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment','resr','2019-03-29 03:26:42',NULL,1),(15,'1553830709449965',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn8itqgx0?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment#_rnd1553830031946','res','2019-03-29 03:38:29',NULL,1),(16,'1553830834442862',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6489202878/Hn8itqgx0?from=page_1005056489202878_profile&wvr=6&mod=weibotime&type=comment#_rnd1553830031946','ssss','2019-03-29 03:40:34',NULL,0),(17,'1553929174069132',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6904395896/HnjhOrUMP?from=page_1005056904395896_profile&wvr=6&mod=weibotime&type=comment','sdfsd','2019-03-30 06:59:34',NULL,1),(18,'1553929911094218',1,1,'微博赞',1,100,NULL,10,'https://weibo.com/6904395896/HnjhOrUMP?from=page_1005056904395896_profile&wvr=6&mod=weibotime&type=comment','tesstststsssssssssssssssssss','2019-03-30 07:11:51',NULL,1);
/*!40000 ALTER TABLE `orders_weibo_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderslog_weibo_comment`
--

DROP TABLE IF EXISTS `orderslog_weibo_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderslog_weibo_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL COMMENT '微博评论订单表(orders_weibo_comment)主键',
  `comments` text,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微博评论订单处理日志。用于管理员查看用户的订单处理情况。如果订单只处理了部分，可在此处看到，并由管理员去给用户补一笔订单。另一方面，也可以防止用户讹诈，谎称数量不对';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderslog_weibo_comment`
--

LOCK TABLES `orderslog_weibo_comment` WRITE;
/*!40000 ALTER TABLE `orderslog_weibo_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `orderslog_weibo_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderslog_weibo_comment_like`
--

DROP TABLE IF EXISTS `orderslog_weibo_comment_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderslog_weibo_comment_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL COMMENT '微博评论赞订单表(orders_weibo_comments_like)主键',
  `comments` text,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微博评论赞订单处理日志。用于管理员查看用户的订单处理情况。如果订单只处理了部分，可在此处看到，并由管理员去给用户补一笔订单。另一方面，也可以防止用户讹诈，谎称数量不对';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderslog_weibo_comment_like`
--

LOCK TABLES `orderslog_weibo_comment_like` WRITE;
/*!40000 ALTER TABLE `orderslog_weibo_comment_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `orderslog_weibo_comment_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderslog_weibo_follow`
--

DROP TABLE IF EXISTS `orderslog_weibo_follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderslog_weibo_follow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL COMMENT '微博关注订单表(orders_weibo_follow)主键',
  `comments` text,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微博关注订单处理日志。用于管理员查看用户的订单处理情况。如果订单只处理了部分，可在此处看到，并由管理员去给用户补一笔订单。另一方面，也可以防止用户讹诈，谎称数量不对';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderslog_weibo_follow`
--

LOCK TABLES `orderslog_weibo_follow` WRITE;
/*!40000 ALTER TABLE `orderslog_weibo_follow` DISABLE KEYS */;
/*!40000 ALTER TABLE `orderslog_weibo_follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderslog_weibo_forward`
--

DROP TABLE IF EXISTS `orderslog_weibo_forward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderslog_weibo_forward` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL COMMENT '微博转发订单表(orders_weibo_forward)主键',
  `comments` text,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微博转发订单处理日志。用于管理员查看用户的订单处理情况。如果订单只处理了部分，可在此处看到，并由管理员去给用户补一笔订单。另一方面，也可以防止用户讹诈，谎称数量不对';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderslog_weibo_forward`
--

LOCK TABLES `orderslog_weibo_forward` WRITE;
/*!40000 ALTER TABLE `orderslog_weibo_forward` DISABLE KEYS */;
/*!40000 ALTER TABLE `orderslog_weibo_forward` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderslog_weibo_like`
--

DROP TABLE IF EXISTS `orderslog_weibo_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderslog_weibo_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL COMMENT '微博赞订单表(orders_weibo_like)主键',
  `comments` text,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='微博赞订单处理日志。用于管理员查看用户的订单处理情况。如果订单只处理了部分，可在此处看到，并由管理员去给用户补一笔订单。另一方面，也可以防止用户讹诈，谎称数量不对';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderslog_weibo_like`
--

LOCK TABLES `orderslog_weibo_like` WRITE;
/*!40000 ALTER TABLE `orderslog_weibo_like` DISABLE KEYS */;
INSERT INTO `orderslog_weibo_like` VALUES (1,1,'已完成点赞数：2，还差点赞数：98','2019-03-22 06:33:46'),(2,7,'已完成点赞数：1，还差点赞数：99','2019-03-28 09:00:23'),(3,9,'已完成点赞数：0，还差点赞数：100','2019-03-29 02:59:35'),(4,11,'已完成点赞数：0，还差点赞数：100','2019-03-29 03:06:25'),(5,14,'已完成点赞数：0，还差点赞数：100','2019-03-29 03:26:43'),(6,15,'已完成点赞数：0，还差点赞数：100','2019-03-29 03:38:46'),(7,17,'已完成点赞数：0，还差点赞数：100','2019-03-30 06:59:39'),(8,18,'已完成点赞数：0，还差点赞数：100','2019-03-30 07:12:07');
/*!40000 ALTER TABLE `orderslog_weibo_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `source` tinyint(1) NOT NULL,
  `types` tinyint(1) DEFAULT NULL,
  `price` decimal(10,0) DEFAULT NULL,
  `comments` text,
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL COMMENT '来源。1：微博',
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id_uindex` (`id`),
  UNIQUE KEY `product_types_uindex` (`types`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COMMENT='产品表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'微博赞',1,1,10,'微博赞，单价1001','2019-01-07 04:38:10','2019-01-07 10:29:01'),(2,'评论赞',1,2,200,'评论赞,200','2019-01-07 09:00:49',NULL),(3,'微博评论',1,3,100,'微博评论产品','2019-03-13 08:01:36',NULL),(4,'微博转发',1,4,300,'微博转发产品，单价300','2019-03-13 08:03:21',NULL),(5,'微博加粉',1,5,100,'微博加粉产品，单价100','2019-03-13 08:03:44',NULL);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_menu`
--

DROP TABLE IF EXISTS `sys_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fid` int(11) DEFAULT '0',
  `power_id` int(11) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `url` varchar(45) DEFAULT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `sort` tinyint(2) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sys_menu_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8 COMMENT='系统菜单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_menu`
--

LOCK TABLES `sys_menu` WRITE;
/*!40000 ALTER TABLE `sys_menu` DISABLE KEYS */;
INSERT INTO `sys_menu` VALUES (1,0,0,'系统管理',NULL,'layui-icon-set-fill',99,'2019-01-06 18:11:50','2019-01-07 04:20:01'),(2,1,0,'菜单管理','/system/menu/list/',NULL,4,'2019-01-06 18:11:53','2019-01-07 03:59:43'),(3,1,0,'权限管理','/system/power/list/',NULL,3,'2019-01-07 02:35:16','2019-01-07 03:59:36'),(4,0,2,'微博管理',NULL,'layui-icon-login-weibo',98,'2019-01-07 03:35:58',NULL),(5,0,3,'个人中心',NULL,'layui-icon-friends',50,'2019-01-07 03:37:18','2019-01-07 04:20:41'),(6,0,4,'微博营销',NULL,'layui-icon-login-weibo',30,'2019-01-07 03:38:03',NULL),(8,1,0,'用户管理','/system/user/list/',NULL,2,'2019-01-07 03:59:18',NULL),(9,1,0,'角色管理','/system/role/list/',NULL,1,'2019-01-07 04:00:04',NULL),(10,4,2,'账号管理','/weibo/account/list/',NULL,1,'2019-01-07 04:24:16',NULL),(11,4,2,'产品列表','/weibo/product/list/',NULL,2,'2019-01-07 04:26:02',NULL),(12,5,3,'个人信息','/user/info/',NULL,1,'2019-01-07 04:26:55',NULL),(13,5,3,'修改密码','/user/pwd/',NULL,2,'2019-01-07 04:27:20',NULL),(14,5,3,'我的订单','/user/orders/',NULL,3,'2019-01-07 04:27:46','2019-01-31 11:04:57'),(15,5,3,'消费记录','/user/log/consume/',NULL,4,'2019-01-07 04:28:07','2019-01-07 04:28:38'),(16,5,3,'充值记录','/user/log/charge/',NULL,5,'2019-01-07 04:28:28',NULL),(17,6,4,'微博赞','/marketing/weibo/like/',NULL,1,'2019-01-07 04:29:30',NULL),(18,6,4,'评论赞','/marketing/weibo/comment/like/',NULL,2,'2019-01-07 04:29:49','2019-03-13 08:23:17'),(19,0,6,'数据管理',NULL,'layui-icon-website',98,'2019-01-31 08:48:09','2019-01-31 08:54:18'),(20,19,6,'用户订单','/datas/user/orders/',NULL,1,'2019-01-31 08:56:25','2019-01-31 08:58:33'),(21,19,6,'用户订单日志','/datas/user/orders/log/',NULL,2,'2019-01-31 08:57:24','2019-03-14 08:19:59'),(22,19,6,'用户消费日志','/datas/user/consume/log/',NULL,3,'2019-01-31 08:58:09','2019-03-14 09:37:00'),(23,19,6,'用户充值日志','/datas/user/charge/log/',NULL,4,'2019-01-31 08:59:05','2019-03-14 09:37:07'),(24,6,4,'微博评论','/marketing/weibo/comment/',NULL,3,'2019-03-13 08:19:50',NULL),(25,6,4,'微博转发','/marketing/weibo/forward/',NULL,4,'2019-03-13 08:20:26',NULL),(26,6,4,'微博关注','/marketing/weibo/follow/',NULL,5,'2019-03-13 08:21:11',NULL);
/*!40000 ALTER TABLE `sys_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_power`
--

DROP TABLE IF EXISTS `sys_power`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_power` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mark` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `comments` text,
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sys_power_id_uindex` (`id`),
  UNIQUE KEY `mark_UNIQUE` (`mark`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COMMENT='系统权限表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_power`
--

LOCK TABLES `sys_power` WRITE;
/*!40000 ALTER TABLE `sys_power` DISABLE KEYS */;
INSERT INTO `sys_power` VALUES (2,'WEIBO_MANAGE','微博管理','一般管理员和超级管理员都有该权限','2019-01-07 03:11:31',NULL),(3,'USER_CENTER','个人中心','所有用户都有该权限','2019-01-07 03:24:46',NULL),(4,'MARKETING_WEIBO','微博营销','所有用户都有该权限','2019-01-07 03:25:26',NULL),(5,'CHARGE_MANAGE','充值管理','所有用户都有该权限','2019-01-07 03:39:31',NULL),(6,'DATA_MANAGE','数据管理','用于网站数据的查询和维护','2019-01-31 08:45:26','2019-01-31 08:52:33');
/*!40000 ALTER TABLE `sys_power` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_role`
--

DROP TABLE IF EXISTS `sys_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `power_ids` varchar(200) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL COMMENT '角色名',
  `types` tinyint(1) unsigned DEFAULT NULL COMMENT '角色类型。99：超级管理员；98：一般管理员；1：普通用户',
  `comments` text COMMENT '备注',
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COMMENT='系统角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role`
--

LOCK TABLES `sys_role` WRITE;
/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES (1,'','超级管理员',99,'超级管理员，拥有所有权限','2019-01-06 23:02:01','2019-03-20 11:00:32'),(2,'2,3,4,5,6,','客服',98,'普通管理员，拥有除“系统管理”外的所有权限','2019-01-06 23:02:06','2019-03-14 10:28:24'),(3,'5,4,3,','一般用户',1,'这是一般用户','2019-01-06 23:02:08','2019-03-22 02:28:55'),(4,'2,3,4,6,','运营',98,NULL,'2019-03-14 10:28:38',NULL),(5,'2,3,4,5,6,','开发',98,NULL,'2019-03-14 10:34:30',NULL);
/*!40000 ALTER TABLE `sys_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fid` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `balance` decimal(20,0) DEFAULT '0',
  `gender` tinyint(1) DEFAULT NULL,
  `tel` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `comments` text,
  `real_name` varchar(50) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL,
  `enable` tinyint(1) unsigned DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `sys_user_id_uindex` (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='系统用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES (1,NULL,1,'admin','1a715028f83dec9530fccb08efa888b3',0,NULL,NULL,NULL,'超管',NULL,NULL,'2019-06-10 02:34:35',NULL,1),(2,NULL,3,'payment','1a715028f83dec9530fccb08efa888b3',99990000,NULL,NULL,NULL,'支付账户，所有用户的钱都是从这个账户出去的',NULL,NULL,'2019-06-10 03:24:00',NULL,0),(3,NULL,4,'haolihua','1a715028f83dec9530fccb08efa888b3',10000,NULL,NULL,NULL,'运营：郝利华',NULL,NULL,'2019-06-10 03:26:02',NULL,1);
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_charge_log`
--

DROP TABLE IF EXISTS `sys_user_charge_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_user_charge_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `comments` text,
  `amount` decimal(10,0) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sys_user_charge_log_id_uindex` (`id`),
  KEY `sys_user_charge_log_user_id_index` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='充值日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_charge_log`
--

LOCK TABLES `sys_user_charge_log` WRITE;
/*!40000 ALTER TABLE `sys_user_charge_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_user_charge_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_consume_log`
--

DROP TABLE IF EXISTS `sys_user_consume_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_user_consume_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `comments` text,
  `amount` decimal(10,0) DEFAULT NULL COMMENT '消费金额',
  `create_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sys_user_consume_log_id_uindex` (`id`),
  KEY `sys_user_consume_log_user_id_index` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COMMENT='用户消费日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_consume_log`
--

LOCK TABLES `sys_user_consume_log` WRITE;
/*!40000 ALTER TABLE `sys_user_consume_log` DISABLE KEYS */;
INSERT INTO `sys_user_consume_log` VALUES (1,1,'购买“微博赞”产品，订单号为：1553236413832816',1000,'2019-03-22 06:33:34'),(2,1,'购买“微博赞”产品，订单号为：1553759179779996',1000,'2019-03-28 07:46:20'),(3,1,'购买“微博赞”产品，订单号为：1553759522040840',1000,'2019-03-28 07:52:02'),(4,1,'购买“微博赞”产品，订单号为：1553761566476521',1000,'2019-03-28 08:26:06'),(5,1,'购买“微博赞”产品，订单号为：1553761674004093',1000,'2019-03-28 08:27:54'),(6,1,'购买“微博赞”产品，订单号为：1553761796301147',1000,'2019-03-28 08:29:56'),(7,1,'购买“微博赞”产品，订单号为：1553763609006085',1000,'2019-03-28 09:00:09'),(8,1,'购买“微博赞”产品，订单号为：1553828221834103',1000,'2019-03-29 02:57:02'),(9,1,'购买“微博赞”产品，订单号为：1553828343535539',1000,'2019-03-29 02:59:04'),(10,1,'购买“微博赞”产品，订单号为：1553828443992037',1000,'2019-03-29 03:00:44'),(11,1,'购买“微博赞”产品，订单号为：1553828771054229',1000,'2019-03-29 03:06:11'),(12,1,'购买“微博赞”产品，订单号为：1553829732145966',1000,'2019-03-29 03:22:12'),(13,1,'购买“微博赞”产品，订单号为：1553829838682740',1000,'2019-03-29 03:23:59'),(14,1,'购买“微博赞”产品，订单号为：1553830001890841',1000,'2019-03-29 03:26:42'),(15,1,'购买“微博赞”产品，订单号为：1553830709449965',1000,'2019-03-29 03:38:29'),(16,1,'购买“微博赞”产品，订单号为：1553830834442862',1000,'2019-03-29 03:40:34'),(17,1,'购买“微博赞”产品，订单号为：1553929174069132',1000,'2019-03-30 06:59:34'),(18,1,'购买“微博赞”产品，订单号为：1553929911094218',1000,'2019-03-30 07:11:51');
/*!40000 ALTER TABLE `sys_user_consume_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weibo_account`
--

DROP TABLE IF EXISTS `weibo_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weibo_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `uniqueid` varchar(20) DEFAULT NULL COMMENT '微博唯一标识id',
  `userdomain` varchar(50) DEFAULT NULL,
  `comments` text,
  `cookies` text,
  `islogin` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0:未登录；1：已登录',
  `last_login_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '上一次成功登录的时间',
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL,
  `valid` tinyint(1) DEFAULT '1' COMMENT '微博是否有效。0：无效；1：有效。默认有效',
  PRIMARY KEY (`id`),
  UNIQUE KEY `weibo_account_id_uindex` (`id`),
  UNIQUE KEY `weibo_account_username_uindex` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8 COMMENT='微博账号表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weibo_account`
--

LOCK TABLES `weibo_account` WRITE;
/*!40000 ALTER TABLE `weibo_account` DISABLE KEYS */;
INSERT INTO `weibo_account` VALUES (2,'15736947596','oarlWPvamn2MWWy8Ho8kBA==\n','6489202878','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:04','2019-01-07 08:40:46',NULL,1),(3,'17077754515','oarlWPvamn2MWWy8Ho8kBA==\n','6163578200','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:15','2019-01-07 08:41:07',NULL,1),(4,'15867063047','oarlWPvamn2MWWy8Ho8kBA==\n','3828941190',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-01-07 08:41:24','2019-01-30 07:57:41',1),(5,'13212800251','5ncX2njKsneLYOmUX+bufg==\n','6579632021',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-02-02 00:13:31',NULL,1),(6,'13234965272','Dh3iOmIB+auXgKf6gyjmtQ==\n','6579631527',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-02-02 00:13:46',NULL,1),(7,'13206532052','R3bqbeDKLgWx6GM03YfDNg==\n','6579993310',NULL,NULL,'',0,'2019-03-07 13:43:08','2019-02-02 00:14:02',NULL,1),(8,'15694511764','LuDkoBjySp1PVJ8OYEdqoA==\n','6579993339',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-02-02 00:14:18',NULL,1),(9,'15694511806','30z/zutKnTKxqMbjUyBhUg==\n','6579994618',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-02-02 00:14:31',NULL,1),(10,'17018971461','8vnor1fWWA6NTKPu/eKQbw==\n','6579994683',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-02-02 00:14:45',NULL,1),(11,'18145711090','xdaDPCG2JH0N2HWo1sVgKg==\n','6579216873',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-02-02 00:14:59',NULL,1),(12,'18145741672','sW1PuK6dFx19wiKVL1HB4g==\n','6579216878',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-02-02 00:15:15',NULL,1),(13,'18145711906','nZhwmN5xOZVKriVuZ61wWg==\n','6579216954',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-02-02 00:15:30',NULL,1),(14,'17018972542','CqrUwzOYBLSUmtNFDW1wug==\n','6579606967',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-02-02 00:15:43',NULL,1),(15,'17096014176','oarlWPvamn2MWWy8Ho8kBA==\n','6547229836',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-02-18 02:23:48',NULL,1),(16,'13751348766','oarlWPvamn2MWWy8Ho8kBA==\n','7014267977',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-03-06 10:44:18',NULL,1),(17,'13684924703','oarlWPvamn2MWWy8Ho8kBA==\n','7014906579',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-03-06 10:44:31',NULL,1),(18,'17875430699','oarlWPvamn2MWWy8Ho8kBA==\n','7014906650',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-03-06 10:44:48',NULL,1),(19,'13620161972','oarlWPvamn2MWWy8Ho8kBA==\n','7014268102',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-03-06 10:45:01',NULL,1),(20,'18320165485','oarlWPvamn2MWWy8Ho8kBA==\n','7014268111',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-03-06 10:45:12',NULL,1),(21,'13416095704','oarlWPvamn2MWWy8Ho8kBA==\n','7014906662',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-03-06 10:45:26',NULL,1),(22,'15088103246','oarlWPvamn2MWWy8Ho8kBA==\n','7014268129',NULL,NULL,'',0,'2019-03-07 13:43:07','2019-03-06 10:45:38',NULL,1),(23,'13711880946','oarlWPvamn2MWWy8Ho8kBA==\n','7014268202','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:17','2019-03-06 10:45:51',NULL,1),(24,'13642929574','oarlWPvamn2MWWy8Ho8kBA==\n','7014906738','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:18','2019-03-06 10:46:00',NULL,1),(25,'13412869965','oarlWPvamn2MWWy8Ho8kBA==\n','7014268228','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:19','2019-03-06 10:46:12',NULL,1),(26,'15112509979','oarlWPvamn2MWWy8Ho8kBA==\n','7014907462','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:21','2019-03-06 13:34:52',NULL,1),(27,'15089367135','oarlWPvamn2MWWy8Ho8kBA==\n','7014907529','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:22','2019-03-06 13:35:07',NULL,1),(28,'13428473145','oarlWPvamn2MWWy8Ho8kBA==\n','7014907584','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:24','2019-03-06 13:35:17',NULL,1),(29,'15915405854','oarlWPvamn2MWWy8Ho8kBA==\n','7014269103','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:25','2019-03-06 13:35:30',NULL,1),(30,'14770065113','oarlWPvamn2MWWy8Ho8kBA==\n','7014269116','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:27','2019-03-06 13:35:40',NULL,1),(31,'15707632629','oarlWPvamn2MWWy8Ho8kBA==\n','7014269125','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:28','2019-03-06 13:35:54',NULL,1),(32,'13544383059','oarlWPvamn2MWWy8Ho8kBA==\n','7014907598','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:29','2019-03-06 13:36:08',NULL,1),(33,'15728735464','oarlWPvamn2MWWy8Ho8kBA==\n','7014269158','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:30','2019-03-06 13:36:19',NULL,1),(34,'13532502798','oarlWPvamn2MWWy8Ho8kBA==\n','7014269165','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:32','2019-03-06 13:36:28',NULL,1),(35,'18318907455','oarlWPvamn2MWWy8Ho8kBA==\n','7014269193','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:33','2019-03-06 13:36:39',NULL,1),(36,'17046761408','oarlWPvamn2MWWy8Ho8kBA==\n','6902100184','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:34','2019-03-06 14:16:07',NULL,1),(37,'17128703240','oarlWPvamn2MWWy8Ho8kBA==\n','6902100728','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:35','2019-03-06 14:16:17',NULL,1),(38,'17042405249','oarlWPvamn2MWWy8Ho8kBA==\n','6902101086','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:37','2019-03-06 14:16:29',NULL,1),(39,'17042404241','oarlWPvamn2MWWy8Ho8kBA==\n','6902101658','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:38','2019-03-06 14:16:41',NULL,1),(40,'17124627364','oarlWPvamn2MWWy8Ho8kBA==\n','6902103316','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:40','2019-03-06 14:16:55',NULL,1),(41,'17042404851','oarlWPvamn2MWWy8Ho8kBA==\n','6901433378','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:41','2019-03-06 14:17:04',NULL,1),(42,'17048809473','oarlWPvamn2MWWy8Ho8kBA==\n','6901433953','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:44','2019-03-06 14:17:16',NULL,1),(43,'17123547340','oarlWPvamn2MWWy8Ho8kBA==\n','6902107559','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:46','2019-03-06 14:17:28',NULL,1),(44,'17129264874','oarlWPvamn2MWWy8Ho8kBA==\n','6902116148','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:48','2019-03-06 14:17:40',NULL,1),(45,'17121228846','oarlWPvamn2MWWy8Ho8kBA==\n','6902118615','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:50','2019-03-06 14:17:49',NULL,1),(46,'0085265803870','oarlWPvamn2MWWy8Ho8kBA==\n','7017343493','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:52','2019-03-06 14:36:21',NULL,1),(47,'0085253438455','oarlWPvamn2MWWy8Ho8kBA==\n','7016678626','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:54','2019-03-06 14:36:37',NULL,1),(48,'17042408451','oarlWPvamn2MWWy8Ho8kBA==\n','6902119744','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:57','2019-03-07 03:48:10',NULL,1),(49,'17124624014','oarlWPvamn2MWWy8Ho8kBA==\n','6902665917','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:40:59','2019-03-07 03:48:21',NULL,1),(50,'17165224137','oarlWPvamn2MWWy8Ho8kBA==\n','6902131018','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:01','2019-03-07 03:48:37',NULL,1),(51,'17124624075','oarlWPvamn2MWWy8Ho8kBA==\n','6902132675','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:03','2019-03-07 03:48:48',NULL,1),(52,'17042404134','oarlWPvamn2MWWy8Ho8kBA==\n','6902671503','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:05','2019-03-07 03:49:03',NULL,1),(53,'17123548145','oarlWPvamn2MWWy8Ho8kBA==\n','6903558673','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:07','2019-03-08 14:21:20',NULL,1),(54,'17122735040','oarlWPvamn2MWWy8Ho8kBA==\n','6903559399','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:08','2019-03-08 14:21:30',NULL,1),(55,'17123546054','oarlWPvamn2MWWy8Ho8kBA==\n','6903560055','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:09','2019-03-08 14:21:43',NULL,1),(56,'17129266948','oarlWPvamn2MWWy8Ho8kBA==\n','6903560830','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:10','2019-03-08 14:21:54',NULL,1),(57,'17129264451','oarlWPvamn2MWWy8Ho8kBA==\n','6903561453','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:12','2019-03-08 14:22:06',NULL,1),(58,'17042400547','oarlWPvamn2MWWy8Ho8kBA==\n','6904101400','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:13','2019-03-08 14:22:16',NULL,1),(59,'17129264821','oarlWPvamn2MWWy8Ho8kBA==\n','6904102012','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:16','2019-03-08 14:22:31',NULL,1),(60,'17042728480','oarlWPvamn2MWWy8Ho8kBA==\n','6904102913','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:17','2019-03-08 14:22:40',NULL,1),(61,'17123547433','oarlWPvamn2MWWy8Ho8kBA==\n','6903564715','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:18','2019-03-08 14:22:54',NULL,1),(62,'17042728472','oarlWPvamn2MWWy8Ho8kBA==\n','6904104684','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:19','2019-03-08 14:23:04',NULL,1),(63,'17121222241','yjpy4aIwmMXrUhreEzgkug==\n','6903566343','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:06','2019-03-08 14:43:11',NULL,1),(64,'17128702764','yjpy4aIwmMXrUhreEzgkug==\n','6904106427','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:08','2019-03-08 14:43:21',NULL,1),(65,'17042405824','yjpy4aIwmMXrUhreEzgkug==\n','6903568267','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:23','2019-03-08 14:43:36',NULL,1),(66,'17046764211','yjpy4aIwmMXrUhreEzgkug==\n','6903569138','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:24','2019-03-08 14:43:49',NULL,1),(67,'17046765478','yjpy4aIwmMXrUhreEzgkug==\n','6903570016','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:25','2019-03-08 14:44:05',NULL,1),(68,'17042404371','yjpy4aIwmMXrUhreEzgkug==\n','6904110219','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:26','2019-03-08 14:44:14',NULL,1),(69,'17048804069','yjpy4aIwmMXrUhreEzgkug==\n','6904111298','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:28','2019-03-08 14:44:32',NULL,1),(70,'17124624653','yjpy4aIwmMXrUhreEzgkug==\n','6904112351','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:29','2019-03-08 14:44:43',NULL,1),(71,'17042401418','yjpy4aIwmMXrUhreEzgkug==\n','6903573949','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:30','2019-03-08 14:45:02',NULL,1),(72,'17129129745','yjpy4aIwmMXrUhreEzgkug==\n','6904114310','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:31','2019-03-08 14:45:17',NULL,1),(73,'17124025645','yjpy4aIwmMXrUhreEzgkug==\n','6904116507','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:33','2019-03-08 14:46:15',NULL,1),(74,'17128384226','yjpy4aIwmMXrUhreEzgkug==\n','6904117544','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:34','2019-03-08 14:46:30',NULL,1),(75,'17046764233','yjpy4aIwmMXrUhreEzgkug==\n','6903580484','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:09','2019-03-08 14:46:39',NULL,1),(76,'17046763470','yjpy4aIwmMXrUhreEzgkug==\n','6903582963','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:10','2019-03-08 14:46:52',NULL,1),(77,'17048804055','yjpy4aIwmMXrUhreEzgkug==\n','6904125351','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:11','2019-03-08 14:47:01',NULL,1),(78,'17129269904','yjpy4aIwmMXrUhreEzgkug==\n','6904126408','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:39','2019-03-08 14:47:39',NULL,1),(79,'17122734986','yjpy4aIwmMXrUhreEzgkug==\n','6904130200','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:40','2019-03-08 14:47:49',NULL,1),(80,'17129269940','yjpy4aIwmMXrUhreEzgkug==\n','6904133899','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:42','2019-03-08 14:48:03',NULL,1),(81,'17129264383','yjpy4aIwmMXrUhreEzgkug==\n','6903598015','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:43','2019-03-08 14:48:11',NULL,1),(82,'17129126401','yjpy4aIwmMXrUhreEzgkug==\n','6903603763','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:45','2019-03-08 14:48:28',NULL,1),(83,'17122734358','yjpy4aIwmMXrUhreEzgkug==\n','6903605856','?wvr=5&lf=reg',NULL,'',0,'2019-03-12 11:41:46','2019-03-08 14:48:42',NULL,1),(84,'17121226840','yjpy4aIwmMXrUhreEzgkug==\n','6904146456','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:14','2019-03-08 14:48:55',NULL,1),(85,'17129129846','yjpy4aIwmMXrUhreEzgkug==\n','6903608213','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:16','2019-03-08 14:49:09',NULL,1),(86,'17124028794','yjpy4aIwmMXrUhreEzgkug==\n','6903608961','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:17','2019-03-08 14:49:18',NULL,1),(87,'17122734987','yjpy4aIwmMXrUhreEzgkug==\n','6904148690','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:20','2019-03-08 14:49:30',NULL,1),(88,'17124621741','yjpy4aIwmMXrUhreEzgkug==\n','6903610525','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:23','2019-03-08 14:49:38',NULL,1),(89,'17046764030','yjpy4aIwmMXrUhreEzgkug==\n','6904150632','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:25','2019-03-08 14:49:51',NULL,1),(90,'17123549740','yjpy4aIwmMXrUhreEzgkug==\n','6904152013','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:27','2019-03-08 14:50:01',NULL,1),(91,'17042403540','yjpy4aIwmMXrUhreEzgkug==\n','6904153004','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:29','2019-03-08 14:50:19',NULL,1),(92,'17129267048','yjpy4aIwmMXrUhreEzgkug==\n','6904154226','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:31','2019-03-08 14:50:28',NULL,1),(93,'17122734352','yjpy4aIwmMXrUhreEzgkug==\n','6903616238','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:33','2019-03-08 14:50:41',NULL,1),(94,'17128384218','yjpy4aIwmMXrUhreEzgkug==\n','6903617537','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:35','2019-03-08 14:50:48',NULL,1),(95,'17128382614','yjpy4aIwmMXrUhreEzgkug==\n','6903618701','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:37','2019-03-08 14:55:16',NULL,1),(96,'17123549647','yjpy4aIwmMXrUhreEzgkug==\n','6903620183','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:38','2019-03-08 14:55:26',NULL,1),(97,'17123546496','yjpy4aIwmMXrUhreEzgkug==\n','6904160179','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:39','2019-03-08 14:55:42',NULL,1),(98,'17165225574','yjpy4aIwmMXrUhreEzgkug==\n','6904161901','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:41','2019-03-08 14:55:50',NULL,1),(99,'17124624668','yjpy4aIwmMXrUhreEzgkug==\n','6903623799','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:42','2019-03-08 14:56:02',NULL,1),(100,'17128383482','yjpy4aIwmMXrUhreEzgkug==\n','6904163681','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:43','2019-03-08 14:56:09',NULL,1),(101,'17048804064','yjpy4aIwmMXrUhreEzgkug==\n','6903625656','?wvr=5&lf=reg',NULL,'',0,'2019-03-13 19:00:44','2019-03-08 14:56:20',NULL,1),(102,'17123547481','yjpy4aIwmMXrUhreEzgkug==\n','6904165585','?wvr=5&lf=reg',NULL,'',0,'2019-03-21 19:00:04','2019-03-08 14:56:28',NULL,1),(103,'17129125427','oarlWPvamn2MWWy8Ho8kBA==\n','6905030725','?wvr=5&lf=reg',NULL,'{\"ALC\": \"ac%3D27%26bt%3D1553224539%26cv%3D5.0%26et%3D1584760539%26ic%3D1959868029%26login_time%3D1553224538%26scf%3D%26uid%3D6905030725%26vf%3D0%26vs%3D0%26vt%3D0%26es%3Dcd89bdb00858a03ca069321e1f690bdc\", \"LT\": \"1553224539\", \"tgc\": \"TGT-NjkwNTAzMDcyNQ==-1553224539-gz-C05C41175F88E7A27B7BDC512E548508-1\", \"SRF\": \"1553224541\", \"SRT\": \"D.QqHBJZPtTriiO4Mb4cYGS4HziZEZ4ZYuirouPFsHNEYd4qPC4mPpMERt4EPKRcsrAcPJ4bMkTsVuObEZJmYGAsH4N4foT!rtWEH64dYmA3m3dNsmKQSYi-fo*B.vAflW-P9Rc0lR-ykYDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPWQNZMsJdScKmHnVr984cMRd4MITESMi49ndDPIJcYPSrnlMcyoiFPfIOWbJDPKSd0kJcM1OFyHVEbJ5mkoODEfi4noI4HJ5mkoODEfS4oCU-PJ5mjkODEfU!oCNsWBV499Jv77\", \"ALF\": \"1584760539\", \"SCF\": \"AnYxia5gmEzbIySl-DyoJ_ZtR0X1mTe7aFLqp1p_kIQTLzTZ3fQ2KNu73MKOT-njVH31zSrqbbo4t8fxfonDAsI.\", \"SUB\": \"_2A25xkCMMDeRhGeBH61cR8y7LyTmIHXVS5BPErDV8PUNbmtBeLRTmkW9NQc0HGCRTIJ1jM8tRoQhDCq7Y-D9va7j1\", \"SUBP\": \"0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJ4u1ff8BpsJbRdXYDKhVQ5JpX5K2hUgL.Foq4eh-7e05Neo-2dJLoIpYLxKqL1h5L1-BLxKqL1heLBoeLxK-L1hnLBKWAqJi0\", \"sso_info\": \"v02m6alo5qztKWRk5iljoOApY6UkKWRk5iljoOMpZCjjKWRk5SljoOgpZCTgbqYpomziaeVqZmDtLaOk4C1jIOMsI2ziLU=\", \"SSOLoginState\": \"1553224541\", \"SUHB\": \"0xnCFSUbZsVawt\", \"Ugrow-G0\": \"56862bac2f6bf97368b95873bc687eef\"}',1,'2019-03-22 03:15:45','2019-03-13 16:30:00',NULL,1),(104,'17129264913','oarlWPvamn2MWWy8Ho8kBA==\n','6905032307','?wvr=5&lf=reg',NULL,'{\"ALC\": \"ac%3D27%26bt%3D1553221236%26cv%3D5.0%26et%3D1584757236%26ic%3D1779378867%26login_time%3D1553221236%26scf%3D%26uid%3D6905032307%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D56ce29474b437481750e6d7f50e7edb8\", \"LT\": \"1553221236\", \"tgc\": \"TGT-NjkwNTAzMjMwNw==-1553221236-yf-70B8CAA4EC41663C328D70B3994CA780-1\", \"SRF\": \"1553221237\", \"SRT\": \"D.QqHBJZPtTrMSUmMb4cYGS4HziZEZ4ZYu5bBu5ePHNEYd4qPDMGMpMERt4EPKRcsrAcPJP4XpTsVuObEZJmEGTcPrMFWlSrYqMqPJMeBdIPBdUFimNmEb4-bg*B.vAflW-P9Rc0lR-ykYDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPVs4ZHiOcXpUPi8IbHuiryJ5bW6dmtui49ndDPIJcYPSrnlMcyoiFPfIOWbJGfnSdYiJcM1OFyHVEbJ5mjkOmzlS4oCIZHJ5mjkOmHIS4oCINsJ5mkoODmk5!oCIZ!rNQHJdv77\", \"ALF\": \"1584757236\", \"SCF\": \"Aomebwfe_LCHRdh66xXwTCfPouG5SR2AnInBsO7UazKGkQm-ah7Bo5OVQ9rHJVhoaT9afkJ0oNxcESVsjCz0Aq0.\", \"SUB\": \"_2A25xkDYlDeRhGeBH61cR8yzPyzuIHXVS5CDtrDV8PUNbmtBeLUH2kW9NQc0AGjetDgngHsG5LFpV-PVlcDHAeSij\", \"SUBP\": \"0033WrSXqPxfM725Ws9jqgMF55529P9D9W5R2MNh2mSb.Ry7OLzWoXN95JpX5K2hUgL.Foq4eh-7e0z0ehM2dJLoIpYLxK-LB.eLB.2LxK-LBKeLB--LxKqL1-zLB.94IrLX\", \"sso_info\": \"v02m6alo5qztKWRk5SlkKSMpZCkhKWRk5SlkJOMpZCUlKWRk5iljpSIpZCkmbmap6W0iaeVqZmDtLaOk4C1jIOMsoyzgLc=\", \"SSOLoginState\": \"1553221237\", \"SUHB\": \"0vJIsa2T_Kg7TI\", \"login\": \"ee581f3744cecd27ee2ede70f2329010\", \"Ugrow-G0\": \"5b31332af1361e117ff29bb32e4d8439\"}',1,'2019-03-22 02:20:39','2019-03-13 16:30:13',NULL,1),(105,'17129129894','oarlWPvamn2MWWy8Ho8kBA==\n','6904395896','?wvr=5&lf=reg',NULL,'{\"ALC\": \"ac%3D27%26bt%3D1553221161%26cv%3D5.0%26et%3D1584757161%26ic%3D1779378867%26login_time%3D1553221161%26scf%3D%26uid%3D6904395896%26vf%3D0%26vs%3D0%26vt%3D0%26es%3Ddd459d88c44c270823278f3661bedb7a\", \"LT\": \"1553221161\", \"tgc\": \"TGT-NjkwNDM5NTg5Ng==-1553221161-yf-0B20F140C780575E678B8C707F1AB9B5-1\", \"SRF\": \"1553221162\", \"SRT\": \"D.QqHBJZPtTrMTi!Mb4cYGS4HziZES4psOW!P3TeEHNEYd4qPDA3bpMERt4EPKRcsrAcPJPc9qTsVuObEZJmmpVDV-Wru4KFMdUDEadEYEMb4-TcYpMNs8NFEC*B.vAflW-P9Rc0lR-ykYDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPVsSOMuM4HqPdoFdGi6Ue9QdOPw4sM3i49ndDPIJcYPSrnlMcyoiFPfAZvoNpsNJ4koJcM1OFyHVEbJ5mkiOmHIO4noTDPJ5mkoOmH6i4noNrHJ5mklOmH6A!oCU3XrSFJuSX77\", \"ALF\": \"1584757161\", \"SCF\": \"Ah8dfRmKUdevzBGYjlgncYIdSDoF77JRDUfy2KCdo3r-f-JZ-oIAVhKv-h8tUN6yg3xewbtS2q7sGesJ2Vuor3I.\", \"SUB\": \"_2A25xkDZ6DeRhGeBH61YS-SvEwjqIHXVS5CCyrDV8PUNbmtBeLVjskW9NQc0A2p76wNT8dVl1_XXEFU6jhrE-bHaB\", \"SUBP\": \"0033WrSXqPxfM725Ws9jqgMF55529P9D9W5e4yEBsUlFXsonzWY5zSTw5JpX5K2hUgL.Foq4ehB01K-R1Kq2dJLoIpYLxKMLBKML1h5LxKqLBo5L1KBLxKnLBoBLBox4dc9f\", \"ULOGIN_IMG\": \"gz-882ba518b2022cafed9c5422806c5ada181e\", \"sso_info\": \"v02m6alo5qztKWRk5ylkJOcpY6DgKWRk5ilkKOApY6TkKWRk6ClkKOQpZCjkbmbtpm1iaeVqZmDtLaOk4C0jLOktY6DpLY=\", \"SSOLoginState\": \"1553221162\", \"SUHB\": \"0U1JGfu_cFq9SN\", \"login\": \"b956ab2a781575709c4b14df65b7a16b\", \"Ugrow-G0\": \"169004153682ef91866609488943c77f\"}',1,'2019-03-22 02:19:26','2019-03-13 16:30:26',NULL,1),(106,'17123547472','oarlWPvamn2MWWy8Ho8kBA==\n','6905033106','?wvr=5&lf=reg',NULL,'{\"ALC\": \"ac%3D27%26bt%3D1553224484%26cv%3D5.0%26et%3D1584760484%26ic%3D1959868029%26login_time%3D1553224483%26scf%3D%26uid%3D6905033106%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D1f11f1436b2f19ca6e63fe5439cfc180\", \"LT\": \"1553224484\", \"tgc\": \"TGT-NjkwNTAzMzEwNg==-1553224484-gz-D66C71F21BCF065B0B479D2B9FF23BFB-1\", \"SRF\": \"1553224486\", \"SRT\": \"D.QqHBJZPtTriKJ!Mb4cYGS4HziZEZ4ZYuJruu5eEHNEYd4qPCOpspMERt4EPKRcsrAcPJdEBETsVuObEZJmEeNmHtW39rPckhMZSBiPYYdmoiPmWjSDMDdeBB*B.vAflW-P9Rc0lR-ykYDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPWFKQWZKFWaPFMkJ-sGTEPbWbS-Vbbui49ndDPIJcYPSrnlMcyoiFPfIOWbJFPnSdYoJcM1OFyHVEbJ5mklODmp5!oCUqHJ5mkCOmzlV4noJZHJ5mkiODEfS4oCN3Y6P49nQn77\", \"ALF\": \"1584760484\", \"SCF\": \"AivTk8777HgKdkNTPzhyd2VcvxdLyt-h0bXUB7WRxFNE_SSL_7e0NUtVBSAqa6di22q0M2raFGXuqB6x9SkHZTU.\", \"SUB\": \"_2A25xkCN2DeRhGeBH61cR8y3NyzqIHXVS5BO-rDV8PUNbmtBeLXPEkW9NQc0AgHBxwztVkkF6A5XaXLMTGld4CZpA\", \"SUBP\": \"0033WrSXqPxfM725Ws9jqgMF55529P9D9WF9wc8g_Tdm3mGhUevVvrYy5JpX5K2hUgL.Foq4eh-7e0epehq2dJLoIpYLxKnL12zLBo2LxKBLB.qL122LxKML1heLBKxoUJp_\", \"ULOGIN_IMG\": \"gz-67851be3cd050071d71c11607961fce04f6f\", \"sso_info\": \"v02m6alo5qztKWRk6CljoSIpZCjhKWRk5ClkKSYpY6EhKWRk5yljoOMpZCTkaOdprGtiaeVqZmDtLaOk4C1jIOMs4yTgLY=\", \"SSOLoginState\": \"1553224486\", \"SUHB\": \"02MvhTPSDM9rsj\", \"Ugrow-G0\": \"9642b0b34b4c0d569ed7a372f8823a8e\"}',1,'2019-03-22 03:14:47','2019-03-13 16:30:39',NULL,1);
/*!40000 ALTER TABLE `weibo_account` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-07 13:50:25
