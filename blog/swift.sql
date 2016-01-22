-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: swift
-- ------------------------------------------------------
-- Server version	5.5.41-0ubuntu0.14.10.1

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
-- Current Database: `swift`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `swift` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `swift`;

--
-- Table structure for table `TGroup`
--

DROP TABLE IF EXISTS `TGroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TGroup` (
  `tg_id` bigint(20) NOT NULL,
  `group_name` varchar(64) NOT NULL,
  `parent_tg_id` bigint(20) NOT NULL,
  `gen_time` datetime NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`tg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TGroup`
--

LOCK TABLES `TGroup` WRITE;
/*!40000 ALTER TABLE `TGroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `TGroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TGroupSecfieldRelation`
--

DROP TABLE IF EXISTS `TGroupSecfieldRelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TGroupSecfieldRelation` (
  `tur_id` bigint(20) NOT NULL,
  `tg_id` bigint(20) NOT NULL,
  `sf_id` bigint(20) NOT NULL,
  PRIMARY KEY (`tur_id`),
  KEY `tg_id` (`tg_id`),
  KEY `sf_id` (`sf_id`),
  CONSTRAINT `TGroupSecfieldRelation_ibfk_1` FOREIGN KEY (`tg_id`) REFERENCES `TGroup` (`tg_id`),
  CONSTRAINT `TGroupSecfieldRelation_ibfk_2` FOREIGN KEY (`sf_id`) REFERENCES `TSecfield` (`secfield`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TGroupSecfieldRelation`
--

LOCK TABLES `TGroupSecfieldRelation` WRITE;
/*!40000 ALTER TABLE `TGroupSecfieldRelation` DISABLE KEYS */;
/*!40000 ALTER TABLE `TGroupSecfieldRelation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TLog`
--

DROP TABLE IF EXISTS `TLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TLog` (
  `log_id` bigint(20) NOT NULL,
  `op_type` int(11) NOT NULL,
  `content` varchar(200) NOT NULL,
  `tu_id` bigint(20) NOT NULL,
  `gen_time` datetime NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `tu_id` (`tu_id`),
  CONSTRAINT `TLog_ibfk_1` FOREIGN KEY (`tu_id`) REFERENCES `TUser` (`tu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TLog`
--

LOCK TABLES `TLog` WRITE;
/*!40000 ALTER TABLE `TLog` DISABLE KEYS */;
/*!40000 ALTER TABLE `TLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TMeta`
--

DROP TABLE IF EXISTS `TMeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TMeta` (
  `objectid` bigint(20) NOT NULL,
  `object_name` varchar(64) NOT NULL,
  `parent_secl_id` bigint(20) NOT NULL,
  `creator` varchar(64) NOT NULL,
  `gen_time` datetime NOT NULL,
  `path` varchar(64) NOT NULL,
  `obj_type` varchar(64) DEFAULT NULL,
  `Subject` varchar(256) DEFAULT NULL,
  `Description` varchar(256) DEFAULT NULL,
  `Language` varchar(64) DEFAULT NULL,
  `Source` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`objectid`),
  KEY `Index_TMe` (`parent_secl_id`),
  CONSTRAINT `TMeta_ibfk_1` FOREIGN KEY (`parent_secl_id`) REFERENCES `TSeclass` (`parent_secl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TMeta`
--

LOCK TABLES `TMeta` WRITE;
/*!40000 ALTER TABLE `TMeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `TMeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TSecfield`
--

DROP TABLE IF EXISTS `TSecfield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TSecfield` (
  `secfield` bigint(20) NOT NULL,
  `parent_secfd_id` bigint(20) NOT NULL,
  `secfield_name` varchar(64) NOT NULL,
  `gen_time` datetime NOT NULL,
  PRIMARY KEY (`secfield`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TSecfield`
--

LOCK TABLES `TSecfield` WRITE;
/*!40000 ALTER TABLE `TSecfield` DISABLE KEYS */;
/*!40000 ALTER TABLE `TSecfield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TSeclass`
--

DROP TABLE IF EXISTS `TSeclass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TSeclass` (
  `seclassid` bigint(20) NOT NULL,
  `parent_secl_id` bigint(20) NOT NULL,
  `seclass_name` varchar(64) NOT NULL,
  `gen_time` datetime NOT NULL,
  PRIMARY KEY (`seclassid`),
  KEY `Index_pa` (`parent_secl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TSeclass`
--

LOCK TABLES `TSeclass` WRITE;
/*!40000 ALTER TABLE `TSeclass` DISABLE KEYS */;
/*!40000 ALTER TABLE `TSeclass` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TUser`
--

DROP TABLE IF EXISTS `TUser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TUser` (
  `tu_id` bigint(20) NOT NULL,
  `login_name` varchar(64) NOT NULL,
  `password` varchar(64) DEFAULT NULL,
  `username` varchar(64) NOT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `gen_time` datetime NOT NULL,
  `login_time` datetime DEFAULT NULL,
  `last_login_time` datetime DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`tu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TUser`
--

LOCK TABLES `TUser` WRITE;
/*!40000 ALTER TABLE `TUser` DISABLE KEYS */;
/*!40000 ALTER TABLE `TUser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TUserGroupRelation`
--

DROP TABLE IF EXISTS `TUserGroupRelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TUserGroupRelation` (
  `tug_id` bigint(20) NOT NULL,
  `tu_id` bigint(20) NOT NULL,
  `tg_id` bigint(20) NOT NULL,
  PRIMARY KEY (`tug_id`),
  KEY `tu_id` (`tu_id`),
  KEY `tg_id` (`tg_id`),
  CONSTRAINT `TUserGroupRelation_ibfk_1` FOREIGN KEY (`tu_id`) REFERENCES `TUser` (`tu_id`),
  CONSTRAINT `TUserGroupRelation_ibfk_2` FOREIGN KEY (`tg_id`) REFERENCES `TGroup` (`tg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TUserGroupRelation`
--

LOCK TABLES `TUserGroupRelation` WRITE;
/*!40000 ALTER TABLE `TUserGroupRelation` DISABLE KEYS */;
/*!40000 ALTER TABLE `TUserGroupRelation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TUserPolRelation`
--

DROP TABLE IF EXISTS `TUserPolRelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TUserPolRelation` (
  `tur_id` bigint(20) NOT NULL,
  `sf_id` bigint(20) NOT NULL,
  `sc_id` bigint(20) NOT NULL,
  PRIMARY KEY (`tur_id`),
  KEY `sf_id` (`sf_id`),
  KEY `sc_id` (`sc_id`),
  CONSTRAINT `TUserPolRelation_ibfk_2` FOREIGN KEY (`sc_id`) REFERENCES `TSeclass` (`seclassid`),
  CONSTRAINT `TUserPolRelation_ibfk_1` FOREIGN KEY (`sf_id`) REFERENCES `TSecfield` (`secfield`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TUserPolRelation`
--

LOCK TABLES `TUserPolRelation` WRITE;
/*!40000 ALTER TABLE `TUserPolRelation` DISABLE KEYS */;
/*!40000 ALTER TABLE `TUserPolRelation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TUserSecfieldRelation`
--

DROP TABLE IF EXISTS `TUserSecfieldRelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TUserSecfieldRelation` (
  `tur_id` bigint(20) NOT NULL,
  `tu_id` bigint(20) NOT NULL,
  `sf_id` bigint(20) NOT NULL,
  PRIMARY KEY (`tur_id`),
  KEY `tu_id` (`tu_id`),
  KEY `sf_id` (`sf_id`),
  CONSTRAINT `TUserSecfieldRelation_ibfk_1` FOREIGN KEY (`tu_id`) REFERENCES `TUser` (`tu_id`),
  CONSTRAINT `TUserSecfieldRelation_ibfk_2` FOREIGN KEY (`sf_id`) REFERENCES `TSecfield` (`secfield`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TUserSecfieldRelation`
--

LOCK TABLES `TUserSecfieldRelation` WRITE;
/*!40000 ALTER TABLE `TUserSecfieldRelation` DISABLE KEYS */;
/*!40000 ALTER TABLE `TUserSecfieldRelation` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-04-27  1:09:42
