SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(36) NOT NULL,
  `username` varchar(80) NOT NULL,
  `password` varchar(80) NOT NULL,
  `fingerprint` varchar(40) NOT NULL,
  `totpkey` varchar(100) NOT NULL,
  `services` TEXT NOT NULL,
  PRIMARY KEY (`id`)
);

