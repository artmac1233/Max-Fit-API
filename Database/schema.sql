-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: maxfit
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Whey Protein'),(2,'Creatina'),(3,'BCAA'),(4,'Pré-Treino'),(5,'Hipercalórico');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(150) DEFAULT NULL,
  `Email` varchar(150) NOT NULL,
  `Telefone` varchar(20) DEFAULT NULL,
  `Senha` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Arthur Macedo','artmac1233@gmail.com','21997315841','123456');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Clientes_ID` int DEFAULT NULL,
  `Data_Pedido` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `Clientes_ID` (`Clientes_ID`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`Clientes_ID`) REFERENCES `clientes` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(150) DEFAULT NULL,
  `Marca` varchar(150) DEFAULT NULL,
  `Preco` decimal(10,2) DEFAULT NULL,
  `Estoque` int DEFAULT NULL,
  `Categoria_ID` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_categoria` (`Categoria_ID`),
  CONSTRAINT `fk_categoria` FOREIGN KEY (`Categoria_ID`) REFERENCES `categoria` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (1,'Whey Protein 900g','Growth Supplements',129.90,50,1),(2,'Creatina Monohidratada 300g','Max Titanium',89.90,40,2),(3,'BCAA 240 cápsulas','Integralmedica',79.90,30,3),(4,'Pré-Treino 300g','Darkness',99.90,25,4),(5,'Hipercalórico 3kg','Probiótica',149.90,20,5),(6,'Creatina Mono hidratada 1kg','Growth',160.00,30,2),(7,'Pré-Treino Insane Original Fruit Punch 300g','Demons Lab',90.00,30,4);
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produtos_pedidos`
--

DROP TABLE IF EXISTS `produtos_pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos_pedidos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Produtos_ID` int NOT NULL,
  `Pedidos_ID` int NOT NULL,
  `Quantidade` int DEFAULT NULL,
  `Preco_Unitario` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `Pedidos_ID` (`Pedidos_ID`),
  KEY `fk_produto` (`Produtos_ID`),
  CONSTRAINT `fk_produto` FOREIGN KEY (`Produtos_ID`) REFERENCES `produtos` (`ID`),
  CONSTRAINT `produtos_pedidos_ibfk_2` FOREIGN KEY (`Pedidos_ID`) REFERENCES `pedidos` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos_pedidos`
--

LOCK TABLES `produtos_pedidos` WRITE;
/*!40000 ALTER TABLE `produtos_pedidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `produtos_pedidos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-26 21:57:32
