create database IF NOT EXISTS myDB;

use myDB;

DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `fingerprint`;
DROP TABLE IF EXISTS `services`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `password` varchar(80) NOT NULL,
  `email` varchar(40) NOT NULL,
  `key` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
);
INSERT INTO `users` (`id`, `username`, `password`, `email`, `key`) VALUES (1, 'conmeo', 'conmeo','conmeo@gmail.com','test');
INSERT INTO `users` (`id`, `username`, `password`, `email`, `key`) VALUES (2, 'boo', 'boo', 'boo@email.com', 'test2');


CREATE TABLE `fingerprint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `fingerprint` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
);
INSERT INTO `fingerprint` (`id`, `username`, `fingerprint`) VALUES (1, 'conmeo', '23f2104ef04ad0c4f3d9800d2b7ae12a');
INSERT INTO `fingerprint` (`id`, `username`, `fingerprint`) VALUES (2, 'boo',  '23f2104ef04ad0c4f3d9800d2b7ae12a');

CREATE TABLE `services` (
    user_id INT,
    service_name VARCHAR(255),
    PRIMARY KEY (user_id, service_name),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO services (user_id, service_name) VALUES (1, 'thanh');
INSERT INTO services (user_id, service_name) VALUES (1, 'toan');




