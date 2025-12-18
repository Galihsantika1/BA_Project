from scipy.stats import pearsonr

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

