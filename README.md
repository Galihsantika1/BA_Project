# Analisis Pengaruh Brand Ambassador terhadap Keputusan Pembelian

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![Pandas](https://img.shields.io/badge/library-pandas-orange.svg)](https://pandas.pydata.org/)
[![Pingouin](https://img.shields.io/badge/statistics-pingouin-green.svg)](https://pingouin-stats.org/)

## 📌 Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis data kuesioner mengenai pengaruh **Brand Ambassador (X)** terhadap **Keputusan Pembelian (Y)** pada produk susu. Skrip ini dikembangkan sebagai bagian dari modul kustom dalam ekosistem **Odoo 17** untuk mengolah data survei pelanggan secara otomatis.

## 📊 Fitur Utama
- **Automation Data Loading**: Membaca data langsung dari format Excel (.xlsx).
- **Data Cleaning**: Menangani *missing values* secara otomatis dan memvalidasi tipe data responden.
- **Statistik Deskriptif**: Menghitung rata-rata skor laten untuk variabel independen dan dependen.
- **Uji Reliabilitas**: Mengukur konsistensi instrumen menggunakan **Cronbach's Alpha**.

## 🛠️ Tech Stack
- **Bahasa**: Python
- **Libraries**: 
  - `Pandas`: Manipulasi dan analisis struktur data.
  - `NumPy`: Komputasi numerik.
  - `Pingouin`: Analisis statistik tingkat lanjut.
  - `Openpyxl`: Engine pembaca file Excel.

## 📁 Struktur Direktori
```text
Brand-Ambassador-Impact-Analysis/
├── data/
│   └── Pembelian_Susu.xlsx     # Dataset (Data Kuesioner)
├── models/
│   └── BA.py                   # Skrip Analisis Utama
└── README.md                   # Dokumentasi Proyek