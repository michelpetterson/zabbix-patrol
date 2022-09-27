USE zpdb;

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;

DROP TABLE IF EXISTS `zp_alerts`;
CREATE TABLE `zp_alerts` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `CallTime` datetime NOT NULL,
  `CallUser` varchar(20) DEFAULT NULL,
  `CallCount` int(5) DEFAULT NULL,
  `CallAnswered` char(3) NOT NULL,
  `CallTickets` varchar(100) NOT NULL,
  `CallMessageFile` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `zp_events`;
CREATE TABLE `zp_events` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `TriggerTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `TriggerZbxId` int(11) NOT NULL,
  `TriggerZbxLastChange` int(11) NOT NULL,
  `TriggerZbxDesc` varchar(400) NOT NULL,
  `TriggerChecked` char(3) NOT NULL,
  `TriggerZbxHost` char(200) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=23524 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `zp_holidays`;
CREATE TABLE `zp_holidays` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `HolidayDate` DATE NOT NULL,
  `HolidayName` varchar(400) NOT NULL,
  `HolidayDesc` varchar(400) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=23524 DEFAULT CHARSET=utf8;
