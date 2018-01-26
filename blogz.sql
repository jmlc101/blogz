-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Jan 26, 2018 at 12:54 AM
-- Server version: 5.6.34-log
-- PHP Version: 7.1.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `blogz`
--

-- --------------------------------------------------------

--
-- Table structure for table `blog`
--

CREATE TABLE `blog` (
  `id` int(11) NOT NULL,
  `title` varchar(120) DEFAULT NULL,
  `body` varchar(2000) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `pub_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `blog`
--

INSERT INTO `blog` (`id`, `title`, `body`, `owner_id`, `pub_date`) VALUES
(1, 'hello', '1234', 1, '2018-01-25 19:59:34'),
(2, 'Chucks first', 'chucks first post thus far.', 2, '2018-01-25 20:11:30'),
(3, 'well', 'this is neat\r\n', 2, '2018-01-25 20:32:39'),
(4, 'timmy\'s first', 'My first post as timmy', 3, '2018-01-25 20:34:10'),
(5, 'hello', 'hello there', 2, '2018-01-25 22:05:54'),
(6, 'ok', 'ok', 2, '2018-01-25 22:27:45'),
(7, 'class 2.14', 'maybe I should start putting notes here, tha\'d be handy! Lets see how far I can go! If I mad it where the blog size could be much bigger, I could make a class notes site!?', 2, '2018-01-26 00:11:11'),
(8, 'test', 'does everything still work', 2, '2018-01-26 00:28:31'),
(9, 'test', 'does everything still work', 2, '2018-01-26 00:29:06'),
(10, 'Another Test', 'route test', 2, '2018-01-26 00:30:39'),
(11, 'yet Anothera', 'and yet another!', 2, '2018-01-26 00:37:08'),
(12, 'asdfasdfasdfasdfa', 'asdfwaefawef', 2, '2018-01-26 00:37:34'),
(13, 'newpost', 'yet another freaking new post', 2, '2018-01-26 00:41:56'),
(14, 'bobstest', 'bobs in the mix again!', 1, '2018-01-26 00:42:45'),
(15, 'hello', 'Hello World!', 1, '2018-01-26 00:49:06');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(120) DEFAULT NULL,
  `password` varchar(120) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `email`) VALUES
(1, 'bob', '1234', ''),
(2, 'chuck', '4321', ''),
(3, 'timmy', '1234', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `blog`
--
ALTER TABLE `blog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `owner_id` (`owner_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `blog`
--
ALTER TABLE `blog`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `blog`
--
ALTER TABLE `blog`
  ADD CONSTRAINT `blog_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
