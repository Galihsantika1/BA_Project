import pandas as pd
import numpy as np
import os # Impor modul os
from scipy.stats import pearsonr
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
import semopy

# 1. Tentukan path file data Anda
# Tentukan direktori file skrip ini berada (c:\...\galih__ba\models\)
current_dir = os.path.dirname(os.path.abspath(__file__)) 

# ASUMSI: File ada di .../galih__ba/data/Pembelian_Susu.xlsx
file_path = os.path.join(current_dir, '..', 'data', 'Pembelian_Susu.xlsx')


print(f"Mencoba memuat file dari path: {file_path}")
print("--- Tahap 1: Pengumpulan Data dan Pembersihan (Python) ---")

try:
    # Memuat data ke dalam Pandas DataFrame
    data = pd.read_excel(file_path) # Gunakan read_excel untuk file .xlsx
    
    print("Data berhasil dimuat.")
    print("\n5 Baris Data Pertama:")
    print(data.head())
    
    print("\nInformasi Struktur Data:")
    data.info()
    
    # --- PENTING: Pindahkan semua logika analisis di sini ---
    
    # Menyiapkan list nama kolom indikator berdasarkan proposal Anda
    # Brand Ambassador (X)
    ba_cols = [col for col in data.columns if col.startswith('BA')]

    # Keputusan Pembelian (Y)
    pd_cols = [col for col in data.columns if col.startswith('PD')]

    all_indicators = ba_cols + pd_cols
    demographic_cols = [col for col in data.columns if col.startswith('D')] # D1, D2, D3, D4

    print(f"\nKolom BA ditemukan: {ba_cols}")
    print(f"Kolom PD ditemukan: {pd_cols}")
    
    # ... Lanjutkan dengan proses analisis atau statistik Anda di sini ...
    
except FileNotFoundError:
    print(f"\nFATAL ERROR: File tidak ditemukan di path: {file_path}")
    print("Pastikan file 'Pembelian_Susu.xlsx' berada di folder 'data' di root modul galih__ba.")
except Exception as e:
    print(f"\nFATAL ERROR: Terjadi kesalahan saat membaca file: {e}")


    print("\n--- B. Pembersihan Data: Missing Values ---")

# 1. Cek jumlah data yang hilang per kolom
print("Jumlah Missing Values per Kolom:")
print(data.isnull().sum())

# 2. Penanganan Missing Values (Strategi):
# a. Jika jumlah missing values sangat kecil (misalnya < 5% dari total N=100),
#    dan missing values hanya terjadi pada baris (responden) tertentu,
#    strategi yang paling umum untuk data kuesioner adalah menghapus baris tersebut.
#    Ini karena data kuesioner adalah data primer yang sifatnya diskrit (Skala Likert).

# Menghapus baris yang memiliki nilai hilang pada semua kolom indikator
# Ganti baris pembersihan Anda menjadi:
data_clean = data.dropna(subset=all_indicators).copy() # <--- Tambahkan .copy() di sini!
# Ini memastikan data_clean adalah DataFrame baru yang independen.
# ...
# Sekarang, baris 73, 89, dan 92 tidak akan menimbulkan peringatan lagi:
# data_clean[all_indicators] = data_clean[all_indicators].astype(int)
# data_clean['Skor_BA'] = data_clean[ba_cols].mean(axis=1)
# data_clean['Skor_PD'] = data_clean[pd_cols].mean(axis=1)

N_initial = len(data)
N_final = len(data_clean)

print(f"\nJumlah Responden Awal: {N_initial}")
print(f"Jumlah Responden Setelah Pembersihan: {N_final}")
print(f"Responden yang Dihapus: {N_initial - N_final}")

# 3. Konversi Tipe Data
# Pastikan semua kolom indikator bertipe numerik (int/float)
data_clean[all_indicators] = data_clean[all_indicators].astype(int)

# 4. Validasi Jangkauan Jawaban (Outliers/Inconsistent Data)
# Cek apakah semua jawaban indikator berada dalam rentang skala Likert (1 hingga 5)
min_value = data_clean[all_indicators].min().min()
max_value = data_clean[all_indicators].max().max()

print(f"\nNilai Minimum Jawaban: {min_value}")
print(f"Nilai Maksimum Jawaban: {max_value}")

if min_value < 1 or max_value > 5:
    print("PERINGATAN: Ditemukan nilai di luar rentang 1-5. Perlu penanganan outlier!")

    print("\n--- C. Feature Engineering: Pembuatan Skor Konstruk ---")

# Brand Ambassador (X)
data_clean['Skor_BA'] = data_clean[ba_cols].mean(axis=1)

# Keputusan Pembelian (Y)
data_clean['Skor_PD'] = data_clean[pd_cols].mean(axis=1)

print("Skor Laten (Rata-rata):")
print(data_clean[['Skor_BA', 'Skor_PD']].head())

# Uji Statistik Deskriptif Skor Laten
print("\nStatistik Deskriptif Skor Laten:")
print(data_clean[['Skor_BA', 'Skor_PD']].describe().transpose())


# Kolom D4: Apakah anda merupakan penggemar Stray Kids? (Bukan, Casual, Aktif, Hardcore)

# Cek distribusi kelompok penggemar
# 1. Pastikan data_clean sudah ada (setelah dropna/pembersihan missing values)
# 2. Lakukan rename langsung pada data_clean
data_clean.rename(columns={'Apakah anda merupakan penggemar Stray Kids?': 'D4'}, inplace=True)

print("\nDistribusi Kelompok Penggemar (D4):")
# Sekarang kolom 'D4' sudah tersedia di data_clean
print(data_clean['D4'].value_counts())

# 3. Membuat kolom biner 'Is_Fan'
fan_categories = ['Casual', 'Aktif', 'Hardcore']
data_clean['Is_Fan'] = np.where(data_clean['D4'].isin(fan_categories), 1, 0)

print("\nDistribusi Biner Fans vs Non-Fans:")
print(data_clean['Is_Fan'].value_counts())

# Cek kolom untuk memastikan semua sudah benar
print("\nDaftar Kolom Terupdate:")
print(data_clean.columns.tolist())


print("--- Tahap 2: Uji Kualitas Data & EDA (Python) ---")

#---Tahap 2: Uji Kualitas Data & EDA (Python)---

def uji_validitas(df, cols, total_col_name):
    print(f"\n--- Uji Validitas: {total_col_name} ---")
    results = []
    # Hitung total skor untuk konstruk ini
    df[total_col_name] = df[cols].sum(axis=1)
    
    for col in cols:
        # Korelasi antara butir (item) dengan skor total
        r_hitung, p_val = pearsonr(df[col], df[total_col_name])
        # Anggap r_tabel untuk N=100 adalah 0.195
        is_valid = "Valid" if r_hitung > 0.195 else "Tidak Valid"
        results.append({'Item': col, 'r_hitung': round(r_hitung, 4), 'Status': is_valid})
    
    return pd.DataFrame(results)

# Jalankan uji validitas untuk Brand Ambassador dan Keputusan Pembelian
valid_ba = uji_validitas(data_clean, ba_cols, 'Total_BA')
valid_pd = uji_validitas(data_clean, pd_cols, 'Total_PD')

print(valid_ba)
print(valid_pd)



# Uji Reliabilitas untuk Brand Ambassador
alpha_ba = pg.cronbach_alpha(data=data_clean[ba_cols])
print(f"\nCronbach's Alpha (Brand Ambassador): {alpha_ba[0]:.4f}")

# Uji Reliabilitas untuk Keputusan Pembelian
alpha_pd = pg.cronbach_alpha(data=data_clean[pd_cols])
print(f"Cronbach's Alpha (Keputusan Pembelian): {alpha_pd[0]:.4f}")



# Set gaya visualisasi
sns.set(style="whitegrid")

# 1. Visualisasi Distribusi Kelompok Penggemar (D4)
plt.figure(figsize=(8, 5))
sns.countplot(x='D4', data=data_clean, hue='D4', palette='viridis', legend=False)
plt.title('Distribusi Tingkat Penggemar Stray Kids (D4)')
plt.xlabel('Kategori Penggemar')
plt.ylabel('Jumlah Responden')
plt.show()

# 2. Visualisasi Hubungan antara Brand Ambassador dan Keputusan Pembelian
plt.figure(figsize=(8, 6))
sns.regplot(x='Skor_BA', y='Skor_PD', data=data_clean, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('Korelasi Skor Brand Ambassador vs Keputusan Pembelian')
plt.xlabel('Skor Brand Ambassador (X)')
plt.ylabel('Skor Keputusan Pembelian (Y)')
plt.show()



# --- Tahap 3: Pemodelan SEM (Python) ---

# 1. Bersihkan nama kolom di DataFrame (Hapus spasi dan titik)
# Ini mengubah 'BA 1.1' menjadi 'BA11' atau 'BA1.1' menjadi 'BA11'
data_clean.columns = [col.replace(' ', '').replace('.', '') for col in data_clean.columns]

# 2. Definisikan Model (Pastikan nama variabel di sini SAMA PERSIS dengan kolom DataFrame yang sudah bersih)
# Jika 'BA 1.1' sudah diubah jadi 'BA11', maka di sini harus 'BA11'
desc = """
  # Measurement Model
  BA =~ BA11 + BA12 + BA13 + BA21 + BA22 + BA23 + BA31 + BA32 + BA33
  PD =~ PD11 + PD12 + PD21 + PD22 + PD31 + PD32 + PD41 + PD42 + PD43

  # Structural Model
  PD ~ BA
"""

# 3. Inisialisasi dan Fit Model
model = semopy.Model(desc)

# Pastikan fit menggunakan data yang sudah diganti namanya
model.fit(data_clean)
stats = semopy.calc_stats(model)
print("\n--- Fit Indices ---")
print(stats.T)

# 4. Mengambil Hasil Estimasi
estimates = model.inspect()
print("\n--- Hasil Estimasi SEM ---")
print(estimates)

# Filter untuk melihat loading factor (hubungan Laten ke Indikator)
loadings = estimates[estimates['op'] == '~']
print("\n--- Loading Factors (Outer Model) ---")
print(loadings[['lval', 'rval', 'Estimate', 'p-value']])

# Filter untuk melihat Path Coefficient (hubungan antar variabel laten)
path_coeffs = estimates[estimates['op'] == '~']
# Cari baris dimana KeputusanPembelian diprediksi oleh BrandAmbassador
result_h0 = path_coeffs[(path_coeffs['lval'] == 'PD') & (path_coeffs['rval'] == 'BA')]

print("\n--- Hasil Uji Hipotesis H0 ---")
print(result_h0)

# Use .get() or next/iter to safely handle empty data in one line
p_val = result_h0['p-value'].values[0] if not result_h0.empty else None

if p_val is None:
    print("Warning: Hypothesis test returned no results.")
elif p_val < 0.05:
    print("H0 Ditolak: Brand Ambassador berpengaruh signifikan terhadap Keputusan Pembelian.")