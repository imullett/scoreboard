CREATE DATABASE IF NOT EXISTS `ff`;


USE `ff`;

CREATE OR REPLACE TABLE `team` (
    `teamId` INT PRIMARY KEY,
    `teamName` VARCHAR(255) NOT NULL,
    `yahooId` VARCHAR(255) NOT NULL ,
    `manager` VARCHAR(255) NOT NULL
);

CREATE OR REPLACE TABLE `matchup` (
    `matchupId` INT AUTO_INCREMENT PRIMARY KEY,
    `team1Id` INT,
    `team2Id` INT,
    `team3Id` INT,
    `weekNumber` INT
);

CREATE OR REPLACE TABLE `game` (
    `gameId` INT AUTO_INCREMENT PRIMARY KEY,
    `teamId` INT NOT NULL,
    `weekNumber` INT NOT NULL,
    `totalPoints` DOUBLE DEFAULT NULL,
    `projectedPoints` DOUBLE DEFAULT NULL,
    `qb` VARCHAR(255) DEFAULT NULL,
    `qbPoints` DOUBLE DEFAULT NULL,
    `wr1` VARCHAR(255) DEFAULT NULL,
    `wr1Points` DOUBLE DEFAULT NULL,
    `wr2` VARCHAR(255) DEFAULT NULL,
    `wr2Points` DOUBLE DEFAULT NULL,
    `rb1` VARCHAR(255) DEFAULT NULL,
    `rb1Points` DOUBLE DEFAULT NULL,
    `rb2` VARCHAR(255) DEFAULT NULL,
    `rb2Points` DOUBLE DEFAULT NULL,
    `te` VARCHAR(255) DEFAULT NULL,
    `tePoints` DOUBLE DEFAULT NULL,
    `flex` VARCHAR(255) DEFAULT NULL,
    `flexPoints` DOUBLE DEFAULT NULL,
    `kicker` VARCHAR(255) DEFAULT NULL,
    `kickerPoints` DOUBLE DEFAULT NULL,
    `defense` VARCHAR(255) DEFAULT NULL,
    `defensePoints` DOUBLE DEFAULT NULL,
    `bn1` VARCHAR(255) DEFAULT NULL,
    `bn1Points` DOUBLE DEFAULT NULL,
    `bn2` VARCHAR(255) DEFAULT NULL,
    `bn2Points` DOUBLE DEFAULT NULL,
    `bn3` VARCHAR(255) DEFAULT NULL,
    `bn3Points` DOUBLE DEFAULT NULL,
    `bn4` VARCHAR(255) DEFAULT NULL,
    `bn4Points` DOUBLE DEFAULT NULL,
    `lastUpdated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    UNIQUE KEY `UK_game_team_week` (`teamId`, `weekNumber`)
    -- CONSTRAINT `FK_game_team` FOREIGN KEY (`teamId`) REFERENCES `team` (`teamId`)
);

INSERT INTO matchup (team1Id, team2Id, team3Id, weeknumber) VALUES
-- Week 1
(2, 9, 5, 1),
(14, 1, 6, 1),
(12, 10, 8, 1),
(13, 3, 15, 1),
(7, 4, 11, 1),
-- Week 2
(2, 13, 4, 2),
(14, 7, 3, 2),
(12, 9, 11, 2),
(8, 10, 1, 2),
(15, 6, 5, 2),
-- Week 3
(2, 7, 11, 3),
(14, 9, 8, 3),
(12, 4, 15, 3),
(13, 3, 6, 3),
(10, 1, 5, 3),

-- Week 4
(2, 9, 15, 4),
(14, 4, 6, 4),
(12, 3, 10, 4),
(13, 11, 1, 4),
(7, 8, 5, 4),

-- Week 5
(2, 4, 6, 5),
(14, 3, 5, 5),
(12, 11, 9, 5),
(13, 8, 10, 5),
(7, 15, 1, 5),

-- Week 6
(2, 3, 5, 6),
(14, 11, 10, 6),
(12, 8, 1, 6),
(13, 15, 6, 6),
(7, 9, 4, 6),

-- Week 7
(2, 11, 1, 7),
(14, 8, 4, 7),
(12, 7, 10, 7),
(13, 6, 3, 7),
(15, 9, 5, 7),

-- Week 8
(2, 8, 10, 8),
(14, 15, 5, 8),
(12, 6, 4, 8),
(13, 7, 11, 8),
(9, 3, 1, 8),

-- Week 9
(2, 6, 5, 9),
(14, 10, 15, 9),
(12, 9, 8, 9),
(13, 4, 1, 9),
(7, 3, 11, 9),

-- Week 10
(2, 10, 5, 10),
(14, 1, 15, 10),
(12, 3, 8, 10),
(13, 11, 6, 10),
(7, 9, 4, 10),

-- Week 11
(2, 14, 12, 11),
(13, 7, 9, 11),
(4, 3, 11, 11),
(8, 15, 6, 11),
(10, 1, 5, 11),

-- Week 12
(2, 5, 8, 12),
(14, 10, 6, 12),
(12, 11, 15, 12),
(13, 9, 3, 12),
(7, 4, 1, 12),

-- Week 13
(2, 14, 12, 13),
(13, 7, 9, 13),
(4, 3, 11, 13),
(8, 15, 6, 13),
(10, 1, 5, 13);