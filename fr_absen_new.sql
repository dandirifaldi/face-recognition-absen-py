-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: fr_absen
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `absensi`
--

DROP TABLE IF EXISTS `absensi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `absensi` (
  `id_absen` int NOT NULL AUTO_INCREMENT,
  `kode_mk` varchar(10) NOT NULL,
  `absen_mhs` varchar(10) NOT NULL,
  `waktu_absen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tanggal_absen` date NOT NULL,
  PRIMARY KEY (`id_absen`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `absensi`
--

LOCK TABLES `absensi` WRITE;
/*!40000 ALTER TABLE `absensi` DISABLE KEYS */;
INSERT INTO `absensi` VALUES (36,'1','1151800072','2024-01-21 13:38:03','2024-01-21');
/*!40000 ALTER TABLE `absensi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `img_dataset`
--

DROP TABLE IF EXISTS `img_dataset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `img_dataset` (
  `img_id` int NOT NULL AUTO_INCREMENT,
  `img_mahasiswa` varchar(10) NOT NULL,
  PRIMARY KEY (`img_id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `img_dataset`
--

LOCK TABLES `img_dataset` WRITE;
/*!40000 ALTER TABLE `img_dataset` DISABLE KEYS */;
INSERT INTO `img_dataset` VALUES (1,'1151800020'),(2,'1151800020'),(3,'1151800020'),(4,'1151800020'),(5,'1151800020'),(6,'1151800020'),(7,'1151800020'),(8,'1151800020'),(9,'1151800020'),(10,'1151800020'),(11,'1151800020'),(12,'1151800020'),(13,'1151800020'),(14,'1151800020'),(15,'1151800020'),(16,'1151800020'),(17,'1151800020'),(18,'1151800020'),(19,'1151800020'),(20,'1151800020'),(21,'1151800020'),(22,'1151800020'),(23,'1151800020'),(24,'1151800020'),(25,'1151800020'),(26,'1151800020'),(27,'1151800020'),(28,'1151800020'),(29,'1151800020'),(30,'1151800020'),(31,'1151800020'),(32,'1151800020'),(33,'1151800020'),(34,'1151800020'),(35,'1151800020'),(36,'1151800020'),(37,'1151800020'),(38,'1151800020'),(39,'1151800020'),(40,'1151800020'),(41,'1151800020'),(42,'1151800020'),(43,'1151800020'),(44,'1151800020'),(45,'1151800020'),(46,'1151800020'),(47,'1151800020'),(48,'1151800020'),(49,'1151800020'),(50,'1151800020'),(51,'1151800020'),(52,'1151800020'),(53,'1151800020'),(54,'1151800020'),(55,'1151800020'),(56,'1151800020'),(57,'1151800020'),(58,'1151800020'),(59,'1151800020'),(60,'1151800020'),(61,'1151800020'),(62,'1151800020'),(63,'1151800020'),(64,'1151800020'),(65,'1151800020'),(66,'1151800020'),(67,'1151800020'),(68,'1151800020'),(69,'1151800020'),(70,'1151800020'),(71,'1151800020'),(72,'1151800020'),(73,'1151800020'),(74,'1151800020'),(75,'1151800020'),(76,'1151800020'),(77,'1151800020'),(78,'1151800020'),(79,'1151800020'),(80,'1151800020'),(81,'1151800020'),(82,'1151800020'),(83,'1151800020'),(84,'1151800020'),(85,'1151800020'),(86,'1151800020'),(87,'1151800020'),(88,'1151800020'),(89,'1151800020'),(90,'1151800020'),(91,'1151800020'),(92,'1151800020'),(93,'1151800020'),(94,'1151800020'),(95,'1151800020'),(96,'1151800020'),(97,'1151800020'),(98,'1151800020'),(99,'1151800020'),(100,'1151800020'),(101,'1151800072'),(102,'1151800072'),(103,'1151800072'),(104,'1151800072'),(105,'1151800072'),(106,'1151800072'),(107,'1151800072'),(108,'1151800072'),(109,'1151800072'),(110,'1151800072'),(111,'1151800072'),(112,'1151800072'),(113,'1151800072'),(114,'1151800072'),(115,'1151800072'),(116,'1151800072'),(117,'1151800072'),(118,'1151800072'),(119,'1151800072'),(120,'1151800072'),(121,'1151800072'),(122,'1151800072'),(123,'1151800072'),(124,'1151800072'),(125,'1151800072'),(126,'1151800072'),(127,'1151800072'),(128,'1151800072'),(129,'1151800072'),(130,'1151800072'),(131,'1151800072'),(132,'1151800072'),(133,'1151800072'),(134,'1151800072'),(135,'1151800072'),(136,'1151800072'),(137,'1151800072'),(138,'1151800072'),(139,'1151800072'),(140,'1151800072'),(141,'1151800072'),(142,'1151800072'),(143,'1151800072'),(144,'1151800072'),(145,'1151800072'),(146,'1151800072'),(147,'1151800072'),(148,'1151800072'),(149,'1151800072'),(150,'1151800072'),(151,'1151800072'),(152,'1151800072'),(153,'1151800072'),(154,'1151800072'),(155,'1151800072'),(156,'1151800072'),(157,'1151800072'),(158,'1151800072'),(159,'1151800072'),(160,'1151800072'),(161,'1151800072'),(162,'1151800072'),(163,'1151800072'),(164,'1151800072'),(165,'1151800072'),(166,'1151800072'),(167,'1151800072'),(168,'1151800072'),(169,'1151800072'),(170,'1151800072'),(171,'1151800072'),(172,'1151800072'),(173,'1151800072'),(174,'1151800072'),(175,'1151800072'),(176,'1151800072'),(177,'1151800072'),(178,'1151800072'),(179,'1151800072'),(180,'1151800072'),(181,'1151800072'),(182,'1151800072'),(183,'1151800072'),(184,'1151800072'),(185,'1151800072'),(186,'1151800072'),(187,'1151800072'),(188,'1151800072'),(189,'1151800072'),(190,'1151800072'),(191,'1151800072'),(192,'1151800072'),(193,'1151800072'),(194,'1151800072'),(195,'1151800072'),(196,'1151800072'),(197,'1151800072'),(198,'1151800072'),(199,'1151800072'),(200,'1151800072');
/*!40000 ALTER TABLE `img_dataset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jadwal`
--

DROP TABLE IF EXISTS `jadwal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jadwal` (
  `id_jadwal` int NOT NULL AUTO_INCREMENT,
  `kode_mk` varchar(10) NOT NULL,
  `ruangan` varchar(10) NOT NULL,
  `hari` varchar(10) NOT NULL,
  `jam_mulai` time NOT NULL,
  `jam_akhir` time NOT NULL,
  PRIMARY KEY (`id_jadwal`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jadwal`
--

LOCK TABLES `jadwal` WRITE;
/*!40000 ALTER TABLE `jadwal` DISABLE KEYS */;
INSERT INTO `jadwal` VALUES (12,'1','D12','Minggu','19:22:00','21:24:00');
/*!40000 ALTER TABLE `jadwal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mahasiswa`
--

DROP TABLE IF EXISTS `mahasiswa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mahasiswa` (
  `nrp` varchar(10) NOT NULL,
  `nama_mhs` varchar(60) DEFAULT NULL,
  `jenis_kel` varchar(1) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `no_telp` varchar(15) NOT NULL,
  `tmpt_lhr` varchar(20) DEFAULT NULL,
  `tgl_lhr` date DEFAULT NULL,
  `alamat` text,
  `status` varchar(1) NOT NULL,
  `date_added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`nrp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mahasiswa`
--

LOCK TABLES `mahasiswa` WRITE;
/*!40000 ALTER TABLE `mahasiswa` DISABLE KEYS */;
INSERT INTO `mahasiswa` VALUES ('1151800020','Miko','L','miko@gmail.com','654654654','a','2023-07-06','Serpong','1','2023-07-30 09:06:56'),('1151800072','Dandi Rifaldi Aldiansyah','L','dandirif0@gmail.com','021-5527481','bogor','2023-08-01','a','1','2023-08-30 08:27:34');
/*!40000 ALTER TABLE `mahasiswa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mata_kuliah`
--

DROP TABLE IF EXISTS `mata_kuliah`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mata_kuliah` (
  `kode_mk` varchar(10) NOT NULL,
  `nama_mk` varchar(50) NOT NULL,
  `semester` varchar(20) NOT NULL,
  `sks` int NOT NULL,
  `nama_dosen` varchar(50) NOT NULL,
  PRIMARY KEY (`kode_mk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mata_kuliah`
--

LOCK TABLES `mata_kuliah` WRITE;
/*!40000 ALTER TABLE `mata_kuliah` DISABLE KEYS */;
INSERT INTO `mata_kuliah` VALUES ('1','Kalkullus','ganjil 2022/2023',3,'Sulistyowati');
/*!40000 ALTER TABLE `mata_kuliah` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mk_mhs`
--

DROP TABLE IF EXISTS `mk_mhs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mk_mhs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `kode_mk` varchar(10) NOT NULL,
  `nrp` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mk_mhs`
--

LOCK TABLES `mk_mhs` WRITE;
/*!40000 ALTER TABLE `mk_mhs` DISABLE KEYS */;
INSERT INTO `mk_mhs` VALUES (18,'1','1151800020'),(19,'1','1151800072');
/*!40000 ALTER TABLE `mk_mhs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_user`
--

DROP TABLE IF EXISTS `tbl_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_user` (
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) DEFAULT NULL,
  `user_username` varchar(45) DEFAULT NULL,
  `user_password` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_user`
--

LOCK TABLES `tbl_user` WRITE;
/*!40000 ALTER TABLE `tbl_user` DISABLE KEYS */;
INSERT INTO `tbl_user` VALUES (2,'admin','admin@localhost.com','pbkdf2:sha256:600000$Da3qYzAzDlSCOHWT$04e4d2454adbea046a4e19fd9830bf6b40073776cbfa53c4dc80fa76787b3a1d'),(3,'a','a@a','pbkdf2:sha256:600000$UMXCXefQ6n9F6Sxh$f11020d6bd2616c34b582481b208cc7c5692d56887e737a5eb8bebfa38a0aa41');
/*!40000 ALTER TABLE `tbl_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'fr_absen'
--

--
-- Dumping routines for database 'fr_absen'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_createUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(45),
    IN p_username VARCHAR(45),
    IN p_password VARCHAR(225)
)
BEGIN
    if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );
     
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_validateLogin` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(45)
)
BEGIN
    select * from tbl_user where user_username = p_username;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-21 13:44:35
