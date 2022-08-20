-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 27, 2022 at 05:38 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ecommerce`
--

-- --------------------------------------------------------

--
-- Table structure for table `buyer`
--

CREATE TABLE `buyer` (
  `id` int(10) NOT NULL,
  `userid` int(11) NOT NULL,
  `name` varchar(70) NOT NULL,
  `contact` varchar(17) NOT NULL,
  `s_email` varchar(70) NOT NULL,
  `c_address` text NOT NULL,
  `p_address` text NOT NULL,
  `balance` int(11) NOT NULL,
  `image` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `buyer`
--

INSERT INTO `buyer` (`id`, `userid`, `name`, `contact`, `s_email`, `c_address`, `p_address`, `balance`, `image`) VALUES
(2, 4, 'Muhammad Zaman', '03047850473', 'zaman@apple.com', 'Muridke, Pakistan', 'Muridke, Pakistan', 0, '4png'),
(6, 9, 'Huzaifa Usman', '', '', '', '', 0, ''),
(17, 20, 'Usman Ali', '12345213632', 'usman@gmail.com', 'sgahfghdsf', 'asdfgsdhfj', 0, '20jpg');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(10) NOT NULL,
  `buyer_id` int(10) NOT NULL,
  `product_id` int(10) NOT NULL,
  `quantity` int(7) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cart_id`, `buyer_id`, `product_id`, `quantity`, `date`) VALUES
(12, 3, 16, 1, '2022-01-22'),
(16, 4, 5, 2, '2022-01-23'),
(18, 4, 1, 1, '2022-01-24');

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `id` int(15) NOT NULL,
  `product_id` int(10) NOT NULL,
  `buyer_id` int(10) NOT NULL,
  `seller_id` int(10) NOT NULL,
  `order_date` date NOT NULL,
  `shipement` varchar(25) NOT NULL,
  `quantity` int(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`id`, `product_id`, `buyer_id`, `seller_id`, `order_date`, `shipement`, `quantity`) VALUES
(1, 1, 20, 2, '2022-01-27', '', 1),
(2, 7, 20, 2, '2022-01-27', '', 2);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `id` int(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` float NOT NULL,
  `discription` text NOT NULL,
  `discount` float NOT NULL,
  `catagory` varchar(50) NOT NULL,
  `seller_id` int(10) NOT NULL,
  `quantity` int(7) NOT NULL,
  `entry_date` date NOT NULL,
  `rating` int(1) NOT NULL,
  `image` varchar(50) NOT NULL,
  `shipement_charges` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `price`, `discription`, `discount`, `catagory`, `seller_id`, `quantity`, `entry_date`, `rating`, `image`, `shipement_charges`) VALUES
(1, 'iphone 7 plus', 45000, 'hghghj', 1, 'mobiles', 2, 4, '2022-01-18', 0, '1.jpg', 99),
(2, 'Office Wear Gents Check Dress Formal Shirt For Men and Boys', 7500, 'Office Wear Gents Check Dress Formal Shirt For Men and Boys', 0, 'man', 2, 50, '2022-01-21', 0, '2.jpeg', 99),
(3, 'PRO Matte Foundation in every shade', 1500, 'PRO Matte Foundation in every shade', 0, 'man', 2, 120, '2022-01-21', 0, '3.jpg', 99),
(4, 'Men formal dress with embroidery', 15000, 'Men formal dress with embroidery', 0, 'DRESSES', 2, 12, '2022-01-21', 0, '4.jpg', 99),
(5, 'Black formal coat', 3200, 'Back formal coat', 0, 'man', 2, 120, '2022-01-21', 0, '5.jpeg', 99),
(6, 'Huda beauty 2 in 1 liner', 700, 'Huda beauty 2 in 1 liner', 0, 'women', 2, 120, '2022-01-21', 0, '6.jpg', 99),
(7, 'Huda beauty lipsticks bundle', 2400, 'Huda beauty lipsticks bundle', 0, 'women', 2, 12, '2022-01-21', 0, '7.jpg', 99),
(8, 'Benetint cheek and lip stain', 1000, 'Benetint cheek and lip stain', 0, 'women', 2, 12, '2022-01-21', 0, '8.jpg', 99),
(9, 'Men casual black leather jacket', 3500, 'Men casual black leather jacket', 0, 'women', 2, 125, '2022-01-21', 0, '9.jpg', 99),
(10, 'sneakers', 2000, 'sneakers', 0, 'women', 2, 35, '2022-01-21', 0, '10.png', 99),
(11, 'long sneakers', 3500, 'long sneakers', 0, 'women', 2, 35, '2022-01-21', 0, '11.png', 99),
(12, 'tie n die shoes in white', 2000, 'tie n die shoes in white', 0, 'man', 2, 38, '2022-01-21', 0, '12.png', 99),
(13, 'brown sneakers', 2000, 'brown sneakers', 0, 'shoes', 2, 25, '2022-01-22', 0, '13.png', 99),
(14, 'black formal shoes', 9000, 'black formal shoes', 0, 'shoes', 2, 30, '2022-01-22', 0, '14.png', 99),
(15, 'casual slip on shoes for men ', 6000, 'casual slip on shoes for men ', 0, 'shoes', 2, 25, '2022-01-22', 0, '15.png', 99),
(16, 'Apple Wireless Charger', 8500, 'Mega Safe Apple\'s Original Wireless Charger', 0, 'accessories', 3, 25, '2022-01-22', 0, '16.jpg', 99),
(17, 'Sun Glasess', 350, 'Sun Glasses of standard quality.', 10, 'man', 2, 25, '2022-01-25', 0, '17.11', 0),
(18, 'Men Suit', 2399, 'Men\'s Collection', 2, 'man', 2, 12, '2022-01-25', 0, '18.48', 0),
(19, 'Sun Glasess', 120, 'Sun Glasses of normal Quality', 25, 'man', 2, 25, '2022-01-25', 0, '19.11', 0);

-- --------------------------------------------------------

--
-- Table structure for table `seller`
--

CREATE TABLE `seller` (
  `id` int(10) NOT NULL,
  `userid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `contact` varchar(17) NOT NULL,
  `address` varchar(150) NOT NULL,
  `business type` varchar(15) NOT NULL,
  `totalproducts` int(3) NOT NULL,
  `balance` int(10) NOT NULL,
  `image` varchar(50) NOT NULL,
  `rank` varchar(15) NOT NULL,
  `approved` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `seller`
--

INSERT INTO `seller` (`id`, `userid`, `name`, `contact`, `address`, `business type`, `totalproducts`, `balance`, `image`, `rank`, `approved`) VALUES
(2, 2, 'Muhammad Rizwan', '', 'Moh Ahmad Pura Muridke', 'car dealer', 5, 0, '', '0', 0),
(3, 3, 'Muhammad Azhan', '', '', '', 0, 0, '', '', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(10) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(20) NOT NULL,
  `status` varchar(15) NOT NULL,
  `profileStatus` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `status`, `profileStatus`) VALUES
(2, 'bitf19m003@pucit.edu.pk', '123', 'seller', 0),
(3, 'azhan@gmail.com', '12345', 'seller', 0),
(4, 'zaman@gmail.com', '123', 'buyer', 1),
(6, 'admin@emart.com', 'admin', 'admin', 1),
(9, 'bitf19m022@gmail.com', '123', 'buyer', 0),
(20, 'UsmanAli@gmail.com', '123', 'buyer', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `buyer`
--
ALTER TABLE `buyer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `userid` (`userid`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `seller`
--
ALTER TABLE `seller`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `userid` (`userid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `buyer`
--
ALTER TABLE `buyer`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `id` int(15) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `seller`
--
ALTER TABLE `seller`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
