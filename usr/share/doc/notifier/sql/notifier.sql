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

DROP TABLE IF EXISTS `sents_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sents_logs` (
  `id` int(255) unsigned NOT NULL AUTO_INCREMENT,
  `nagios_date` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `contact` longtext COLLATE utf8_bin,
  `host` longtext COLLATE utf8_bin,
  `service` longtext COLLATE utf8_bin,
  `state` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `notification_number` int(11) DEFAULT NULL,
  `method` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `priority` tinyint(1) DEFAULT NULL,
  `matched_rule` longtext COLLATE utf8_bin,
  `exit_code` tinyint(1) DEFAULT NULL,
  `exit_command` longtext COLLATE utf8_bin,
  `epoch` int(255) unsigned DEFAULT NULL,
  `cmd_duration` int(255) unsigned DEFAULT NULL,
  `notifier_duration` int(255) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `type` varchar(255) COLLATE utf8_bin NOT NULL,
  `value` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
LOCK TABLES `configs` WRITE;
/*!40000 ALTER TABLE `configs` DISABLE KEYS */;
INSERT INTO `configs` VALUES 
  (1,'debug','cfg','0'),
  (2,'debug_rules','rules','2'),
  (3,'log_file','cfg','/srv/rgm/notifier/log/notifier.log'),
  (4,'logrules_file','rules','/srv/rgm/notifier/log/notifier_rules.log'),
  (5,'notifsent_file','rules','/srv/rgm/notifier/log/notifier_send.log');
/*!40000 ALTER TABLE `configs` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contacts` (
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `debug` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `methods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `methods` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `type` varchar(255) COLLATE utf8_bin NOT NULL,
  `line` text COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
LOCK TABLES `methods` WRITE;
/*!40000 ALTER TABLE `methods` DISABLE KEYS */;
INSERT INTO `methods` VALUES 
  (1,'email-host','host','/usr/bin/printf \"%b\" \"***** RGM  *****\\\\n\\\\nNotification Type: $NOTIFICATIONTYPE$\\\\nHost: $HOSTNAME$\\\\nState: $HOSTSTATE$\\\\nAddress: $HOSTADDRESS$\\\\nInfo: $HOSTOUTPUT$\\\\n\\\\nDate/Time: $LONGDATETIME$\\\\n\" | /bin/mail -s \"Host $HOSTSTATE$ alert for $HOSTNAME$!\" $CONTACTEMAIL$'),
  (2,'email-service','service','/usr/bin/printf \"%b\" \"*****  RGM *****\\\\n\\\\nNotification Type: $NOTIFICATIONTYPE$\\\\n\\\\nService: $SERVICEDESC$\\\\nHost: $HOSTALIAS$\\\\nAddress: $HOSTADDRESS$\\\\nState: $SERVICESTATE$\\\\n\\\\nDate/Time: $LONGDATETIME$\\\\n\\\\nAdditional Info:\\\\n\\\\n$SERVICEOUTPUT$\" | /bin/mail -s \"Services $SERVICESTATE$ alert for $HOSTNAME$/$SERVICEDESC$!\" $CONTACTEMAIL$'),
  (3,'teams-host','host','/srv/rgm/notifier/var/venv/bin/python3 /srv/rgm/notifier/var/scripts/msteams/PyWebHook.py -t host -H \"$HOSTNAME$\" -a \"$HOSTADDRESS$\" -d \"$LONGDATETIME$\" -o \"$HOSTOUTPUT$\" -S \"$HOSTSTATE$\"'),
  (4,'teams-service','service','/srv/rgm/notifier/var/venv/bin/python3 /srv/rgm/notifier/var/scripts/msteams/PyWebHook.py -t service -H \"$HOSTNAME$\" -a \"$HOSTADDRESS$\" -d \"$LONGDATETIME$\" -o \"$SERVICEOUTPUT$\" -S \"$SERVICESTATE$\" -s \"$SERVICEDESC$\"'),
  (5,'teams-app','service','/srv/rgm/notifier/var/venv/bin/python3 /srv/rgm/notifier/var/scripts/msteams/PyWebHook.py -t application -H \"$HOSTNAME$\" -a \"$HOSTADDRESS$\" -d \"$LONGDATETIME$\" -o \"$SERVICEOUTPUT$\" -S \"$SERVICESTATE$\" -s \"$SERVICEDESC$\"'),
  (6,'teams-prio','service','/srv/rgm/notifier/var/venv/bin/python3 /srv/rgm/notifier/var/scripts/msteams/PyWebHook.py -t application -H \"$HOSTNAME$\" -a \"$HOSTADDRESS$\" -d \"$LONGDATETIME$\" -o \"$SERVICEOUTPUT$\" -S \"$SERVICESTATE$\" -s \"$SERVICEDESC$\" -p'),
  (7,'email-appCRITICAL','service','/usr/bin/printf \"%b\" \"*****  RGM  *****\\\\n\\\\nL Application $SERVICEDESC$ est actuellement indisponible.\\\\n\\\\nInfo: $SERVICEOUTPUT$\\\\n\\\\n\\\\n\\\\nDate/Time : $LONGDATETIME$\\\\n\" | /bin/mail -s \"L application $SERVICEDESC$ est indisponible\" $CONTACTEMAIL$'),(8,'email-appWARNING','service','/usr/bin/printf \"%b\" \"*****  RGM  *****\\\\n\\\\nL Application $SERVICEDESC$ rencontre actuellement quelques perturbations.\\\\n\\\\nNos equipes mettent tout en oeuvre pour resoudre au plus vite le probleme.\\\\n\\\\nInfo: $SERVICEOUTPUT$\\\\n\\\\n\\\\n\\\\nDate/Time : $LONGDATETIME$\\\\n\" | /bin/mail -s \"L application $SERVICEDESC$ est en alerte\" $CONTACTEMAIL$'),(9,'email-appOK','service','/usr/bin/printf \"%b\" \"*****  RGM  *****\\\\n\\\\nL Application $SERVICEDESC$ est revenue a un etat de fonctionnement normal.\\\\n\\\\nElle ne rencontre actuellement plus de perturbations.\\\\n\\\\nInfo: $SERVICEOUTPUT$\\\\n\\\\n\\\\n\\\\nDate/Time : $LONGDATETIME$\\\\n\" | /bin/mail -s \"L application $SERVICEDESC$ est revenue a la normale\" $CONTACTEMAIL$');
/*!40000 ALTER TABLE `methods` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `rule_method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rule_method` (
  `rule_id` bigint unsigned NOT NULL,
  `method_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`rule_id`,`method_id`),
  KEY `rule_id` (`rule_id`),
  KEY `method_id` (`method_id`),
  CONSTRAINT `rule_method_ibfk_1` FOREIGN KEY (`rule_id`) REFERENCES `rules` (`id`),
  CONSTRAINT `rule_method_ibfk_2` FOREIGN KEY (`method_id`) REFERENCES `methods` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;


LOCK TABLES `rule_method` WRITE;
/*!40000 ALTER TABLE `rule_method` DISABLE KEYS */;
INSERT INTO `rule_method` VALUES 
  (1,1),
  (2,1),
  (3,2),
  (4,2);
/*!40000 ALTER TABLE `rule_method` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rules` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `type` varchar(255) COLLATE utf8_bin NOT NULL,
  `debug` tinyint(1) NOT NULL DEFAULT '0',
  `contact` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '*',
  `host` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '*',
  `service` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '*',
  `state` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '*',
  `notificationnumber` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '*',
  `timeperiod_id` bigint(20) unsigned NOT NULL,
  `tracking` tinyint(1) COLLATE utf8_bin NOT NULL DEFAULT '0',
  `sort_key` int(32) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `timeperiod_id` (`timeperiod_id`),
  CONSTRAINT `rules_ibfk_1` FOREIGN KEY (`timeperiod_id`) REFERENCES `timeperiods` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
LOCK TABLES `rules` WRITE;
/*!40000 ALTER TABLE `rules` DISABLE KEYS */;
INSERT INTO `rules` VALUES 
  (1,'HOSTS UP (24x7)','host',0,'*','*','-','UP','*',1,0,0,0),
  (2,'HOSTS ALERTS (24x7)','host',0,'*','*','-','*','1',1,1,0,0),
  (3,'SERVICES OK (24x7)','service',0,'*','*','*','OK','*',1,0,0,0),
  (4,'SERVICES ALERTS (24x7)','service',0,'*','*','*','*','1',1,1,0,0);
/*!40000 ALTER TABLE `rules` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `timeperiods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timeperiods` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `daysofweek` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '*',
  `timeperiod` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '*',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
LOCK TABLES `timeperiods` WRITE;
/*!40000 ALTER TABLE `timeperiods` DISABLE KEYS */;
INSERT INTO `timeperiods` VALUES (1,'24x7','*','*');
/*!40000 ALTER TABLE `timeperiods` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;