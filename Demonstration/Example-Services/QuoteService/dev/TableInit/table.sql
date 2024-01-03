SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `QuoteTable`(`id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT, `quote` text);
INSERT INTO `QuoteTable` (`quote`) VALUES
("The only limit to our realization of tomorrow will be our doubts of today."),
("Success is not final, failure is not fatal: It is the courage to continue that counts."),
("Life is what happens when you're busy making other plans."),
("In three words I can sum up everything I've learned about life: it goes on."),
("The future belongs to those who believe in the beauty of their dreams.");
COMMIT;