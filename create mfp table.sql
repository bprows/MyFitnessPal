drop table if exists mfp.foods;
CREATE TABLE `mfp`.`foods` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `meal` VARCHAR(45) NOT NULL,
  `food` VARCHAR(450),
  `unit` VARCHAR(45),
  `quantity` VARCHAR(45),
  `calories` DECIMAL NULL,
  `carbohydrates` DECIMAL NULL,
  `fat` DECIMAL NULL,
  `protein` DECIMAL NULL,
  `sodium` DECIMAL NULL,
  `sugar` DECIMAL NULL,
  PRIMARY KEY (`id`));


  drop table if exists mfp.weight;
  CREATE TABLE `mfp`.`weight` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `username` VARCHAR(45) NULL,
  `weight` DOUBLE NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);