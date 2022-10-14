-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: localhost    Database: sample_superstore
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `Category`
--

DROP TABLE IF EXISTS `Category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Category` (
  `CategoryId` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`CategoryId`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Category`
--

LOCK TABLES `Category` WRITE;
/*!40000 ALTER TABLE `Category` DISABLE KEYS */;
/*!40000 ALTER TABLE `Category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customer`
--

DROP TABLE IF EXISTS `Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Customer` (
  `CustomerId` int NOT NULL AUTO_INCREMENT,
  `CustomerCode` varchar(255) NOT NULL UNIQUE,
  `CustomerName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`CustomerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer`
--

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Employee`
--

DROP TABLE IF EXISTS `Employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Employee` (
  `EmployeeId` int NOT NULL AUTO_INCREMENT,
  `Designation` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`EmployeeId`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Employee`
--

LOCK TABLES `Employee` WRITE;
/*!40000 ALTER TABLE `Employee` DISABLE KEYS */;
/*!40000 ALTER TABLE `Employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OrderedItems`
--

DROP TABLE IF EXISTS `OrderedItems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `OrderedItems` (
  `OrderedItemId` int NOT NULL AUTO_INCREMENT,
  `OrderId` int NOT NULL,
  `ProductId` int NOT NULL,
  `Quantity` int NOT NULL,
  `Discount` float NOT NULL,
  `Sales` float NOT NULL,
  `Profit` float NOT NULL,
  PRIMARY KEY (`OrderedItemId`),
  KEY `OrderId` (`OrderId`),
  KEY `ProductId` (`ProductId`),
  CONSTRAINT `ordereditems_ibfk_1` FOREIGN KEY (`OrderId`) REFERENCES `Orders` (`OrderId`),
  CONSTRAINT `ordereditems_ibfk_2` FOREIGN KEY (`ProductId`) REFERENCES `Product` (`ProductId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OrderedItems`
--

LOCK TABLES `OrderedItems` WRITE;
/*!40000 ALTER TABLE `OrderedItems` DISABLE KEYS */;
/*!40000 ALTER TABLE `OrderedItems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Orders` (
  `OrderId` int NOT NULL AUTO_INCREMENT,
  `OrderCode` varchar(255) NOT NULL UNIQUE,
  `OrderDate` date NOT NULL,
  `CustomerId` int NOT NULL,
  `ShipmentId` int NOT NULL,
  `SegmentId` int NOT NULL,
  `RegionId` int NOT NULL,
  `Returned` TinyInt(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`OrderId`),
  KEY `CustomerId` (`CustomerId`),
  KEY `RegionId` (`RegionId`),
  KEY `orders_ibfk_3_idx` (`ShipmentId`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`CustomerId`) REFERENCES `Customer` (`CustomerId`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`RegionId`) REFERENCES `RegionalDiv` (`RegionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product`
--

DROP TABLE IF EXISTS `Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product` (
  `ProductId` int NOT NULL AUTO_INCREMENT,
  `ProductName` varchar(255) NOT NULL,
  `ProductCode` varchar(255) NOT NULL,
  `CategoryId` int NOT NULL,
  `SubCategoryId` int NOT NULL,
  PRIMARY KEY (`ProductId`),
  UNIQUE KEY `ProductCode` (`ProductCode`),
  KEY `fk_category_id_idx` (`CategoryId`),
  KEY `fk_sub_category_id_idx` (`SubCategoryId`),
  CONSTRAINT `fk_product_category_id` FOREIGN KEY (`CategoryId`) REFERENCES `Category` (`CategoryId`),
  CONSTRAINT `fk_product_sub_category_id` FOREIGN KEY (`SubCategoryId`) REFERENCES `SubCategory` (`SubCategoryId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product`
--

LOCK TABLES `Product` WRITE;
/*!40000 ALTER TABLE `Product` DISABLE KEYS */;
/*!40000 ALTER TABLE `Product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RegionalDiv`
--

DROP TABLE IF EXISTS `RegionalDiv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RegionalDiv` (
  `RegionId` int NOT NULL AUTO_INCREMENT,
  `ManagerId` int NOT NULL,
  `Region` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`RegionId`),
  UNIQUE KEY `Region` (`Region`),
  KEY `ManagerId` (`ManagerId`),
  CONSTRAINT `regionaldiv_ibfk_1` FOREIGN KEY (`ManagerId`) REFERENCES `Employee` (`EmployeeId`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RegionalDiv`
--

LOCK TABLES `RegionalDiv` WRITE;
/*!40000 ALTER TABLE `RegionalDiv` DISABLE KEYS */;
/*!40000 ALTER TABLE `RegionalDiv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Segment`
--

DROP TABLE IF EXISTS `Segment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Segment` (
  `SegmentId` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  PRIMARY KEY (`SegmentId`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Segment`
--

LOCK TABLES `Segment` WRITE;
/*!40000 ALTER TABLE `Segment` DISABLE KEYS */;
/*!40000 ALTER TABLE `Segment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Shipment`
--

DROP TABLE IF EXISTS `Shipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Shipment` (
  `ShipmentId` int NOT NULL AUTO_INCREMENT,
  `ShipmentDate` date NOT NULL,
  `ShipmentMode` varchar(255) NOT NULL,
  `City` varchar(255) NOT NULL,
  `State` varchar(255) NOT NULL,
  `PostalCode` varchar(255) NOT NULL,
  `Days` int DEFAULT NULL,
  PRIMARY KEY (`ShipmentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Shipment`
--

LOCK TABLES `Shipment` WRITE;
/*!40000 ALTER TABLE `Shipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `Shipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SubCategory`
--

DROP TABLE IF EXISTS `SubCategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SubCategory` (
  `SubCategoryId` int NOT NULL AUTO_INCREMENT,
  `CategoryId` int NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`SubCategoryId`),
  KEY `a_idx` (`CategoryId`),
  CONSTRAINT `fk_category_id` FOREIGN KEY (`CategoryId`) REFERENCES `Category` (`CategoryId`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SubCategory`
--

LOCK TABLES `SubCategory` WRITE;
/*!40000 ALTER TABLE `SubCategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `SubCategory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-13 22:52:21
