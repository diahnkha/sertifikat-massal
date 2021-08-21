-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 11 Jul 2021 pada 18.13
-- Versi server: 10.4.18-MariaDB
-- Versi PHP: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sertifikatresmi`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `daftar_sertifikat`
--

CREATE TABLE `daftar_sertifikat` (
  `no` int(100) NOT NULL,
  `id` varchar(20) NOT NULL,
  `nama` varchar(30) NOT NULL,
  `lembaga` varchar(50) NOT NULL,
  `bukti` varchar(100) NOT NULL,
  `keterangan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `daftar_sertifikat`
--

INSERT INTO `daftar_sertifikat` (`no`, `id`, `nama`, `lembaga`, `bukti`, `keterangan`) VALUES
(1, '111111111', 'Putri Hamsiah Rofi', 'BNI Syariah', 'https://www.instagram.com/pham_rf/', 'berikut link tanda approved dari lembaga resmi tersebut www.instagram.com'),
(2, '22222222', 'Diah Nur Khasanah', 'Dirilis.com', 'https://www.instagram.com/diahnkha/', 'berikut link tanda approved dari lembaga resmi tersebut www.google.com'),
(3, '33333333', 'Abdul Hamid', 'PT Toyota', 'toyota.com', 'berikut link tanda approved dari lembaga resmi tersebut www.toyota.com'),
(4, '44444444', 'Restu Efendi', 'PT Toyota', 'toyota.com', 'berikut link tanda approved dari lembaga resmi tersebut www.toyota.com'),
(5, '55555555', 'Abdul Aziz', 'PT Toyota', 'toyota.com', 'berikut link tanda approved dari lembaga resmi tersebut www.toyota.com'),
(14, '66666666', 'Ibad Urahman', 'Gramedia', 'gramedia.com', 'berikut link tanda approved dari lembaga resmi tersebut www.gramedia.com');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `daftar_sertifikat`
--
ALTER TABLE `daftar_sertifikat`
  ADD PRIMARY KEY (`no`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `daftar_sertifikat`
--
ALTER TABLE `daftar_sertifikat`
  MODIFY `no` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
