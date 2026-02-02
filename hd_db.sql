-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3308
-- Generation Time: Jan 08, 2025 at 09:34 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hd_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `note`
--

CREATE TABLE `note` (
  `id_note` int(11) NOT NULL,
  `nom_txt` varchar(255) NOT NULL,
  `texte` text NOT NULL,
  `image` varchar(255) NOT NULL,
  `date_creation` datetime NOT NULL DEFAULT current_timestamp(),
  `id_user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `note`
--

INSERT INTO `note` (`id_note`, `nom_txt`, `texte`, `image`, `date_creation`, `id_user`) VALUES
(85, 'MY note', 'You remember things betterwhen you write them downby hand.Here\'s why.', 'note1.jpg', '2024-12-31 13:54:22', 12),
(86, 'Social Media', 'IF YOU FInDThis VideoHELPFULPLEASEGIVE it ALike', 'WhatsApp Image 2024-12-25 at 13.15.28 (1).jpeg', '2024-12-31 14:01:20', 12),
(87, 'Phone', 'HelpC CodeJudyterLab t @ Python 3 (pyxernel) )1 (221):sample_data1 = [Your Mobile number has been awarded with a $2880 Bonussample_date2 = [I think I\'m waiting for the same bust Inform me when you get there,if you ever get there. If you are under data3 = [PRIVATE! Your 2004 Account Statement for 0772676999 shows786 unredemed Bonus Points. To claim call 0871918248 Identifier Code: 45239 Expires][251]:def predictor/data):test = pd.Series(data):cleaned_data = test.apply(lambda x-data,cleaning(x))transform_data= cv.transform(cleaned-data)result = le. inverse_transform(multi-nb.predict(transform.data)) [0]return result[261]:predictor(sample,data1][261]: \'spam\'[281]: predictor(sample.data2][281]: \'no_spam\')[291]: \'span\'', 'IMG20241219115546.jpg', '2024-12-31 15:25:58', 12),
(88, 'Python Code', 'HelpC CodeJudyterLab t @ Python 3 (pyxernel) )1 (221):sample_data1 = [Your Mobile number has been awarded with a $2880 Bonussample_date2 = [I think I\'m waiting for the same bust Inform me when you get there,if you ever get there. If you are under data3 = [PRIVATE! Your 2004 Account Statement for 0772676999 shows786 unredemed Bonus Points. To claim call 0871918248 Identifier Code: 45239 Expires][251]:def predictor/data):test = pd.Series(data):cleaned_data = test.apply(lambda x-data,cleaning(x))transform_data= cv.transform(cleaned-data)result = le. inverse_transform(multi-nb.predict(transform.data)) [0]return result[261]:predictor(sample,data1][261]: \'spam\'[281]: predictor(sample.data2][281]: \'no_spam\')[291]: \'span\'', 'IMG20241219115546.jpg', '2025-01-06 02:01:58', 12),
(89, 'Good Life', 'You remember things better when you write them down by hand, Here\'s why.', 'note1.jpg', '2025-01-06 09:16:31', 12),
(90, 'titre', 'this is another mole I wroteThis is another mote I wrote.', 'another_note.jpg', '2025-01-06 15:26:09', 12),
(91, 'titre', 'You remember things betterwhen you write them downby hand.Here\'s why', 'note1.jpg', '2025-01-06 15:59:33', 12);

-- --------------------------------------------------------

--
-- Table structure for table `note_tag`
--

CREATE TABLE `note_tag` (
  `id_note` int(11) NOT NULL,
  `id_tag` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `note_tag`
--

INSERT INTO `note_tag` (`id_note`, `id_tag`) VALUES
(85, 1),
(85, 23),
(86, 24),
(87, 25),
(88, 23),
(89, 23),
(89, 26);

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

CREATE TABLE `tag` (
  `id_tag` int(11) NOT NULL,
  `nom` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tag`
--

INSERT INTO `tag` (`id_tag`, `nom`) VALUES
(1, 'life'),
(23, 'Study'),
(24, 'Media'),
(25, 'Screenshots'),
(26, 'good life');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id_user`, `nom`, `prenom`, `email`, `phone_number`, `password`) VALUES
(12, 'Ihssane', 'NEDJAOUI', 'ihssanenedjaoui5@gmail.com', '0688062914', '$2b$12$NIzb0w6J1JdaN0XblF9gxODEf/J9odnj411krnb0K/L6te9ICowBW'),
(13, 'Ihssane', 'NEDJAOUI', 'ihssanenedjaoui55@gmail.com', '0688062914', '$2b$12$6ZHnuX.Cnex62e4FLMtfeuPjHHwSvHwtVtzA62MAxR9JHu.DtWyZ.'),
(14, 'asma', 'ajg', 'asmae@gmail.com', '0688062914', '$2b$12$CmtFkar4YLDvDOkmLHIW2.aQoH.Tc4WiOlJlpESnpZ8IuIfkZqTkK'),
(15, 'salma', 'salma', 'salma@gmail.com', '0688062914', '$2b$12$fuKAfri0jo2a17SgU/0ZkecxwRcHk.j2usZm6Od1Y9PIn6Xv4z1XS');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `note`
--
ALTER TABLE `note`
  ADD PRIMARY KEY (`id_note`),
  ADD KEY `Test` (`id_user`);

--
-- Indexes for table `note_tag`
--
ALTER TABLE `note_tag`
  ADD KEY `liaison` (`id_note`),
  ADD KEY `liaison2` (`id_tag`);

--
-- Indexes for table `tag`
--
ALTER TABLE `tag`
  ADD PRIMARY KEY (`id_tag`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `note`
--
ALTER TABLE `note`
  MODIFY `id_note` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=92;

--
-- AUTO_INCREMENT for table `tag`
--
ALTER TABLE `tag`
  MODIFY `id_tag` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `note`
--
ALTER TABLE `note`
  ADD CONSTRAINT `Test` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);

--
-- Constraints for table `note_tag`
--
ALTER TABLE `note_tag`
  ADD CONSTRAINT `liaison` FOREIGN KEY (`id_note`) REFERENCES `note` (`id_note`),
  ADD CONSTRAINT `liaison2` FOREIGN KEY (`id_tag`) REFERENCES `tag` (`id_tag`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
