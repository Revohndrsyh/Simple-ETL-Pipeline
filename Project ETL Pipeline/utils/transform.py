import pandas as pd
import numpy as np
from datetime import datetime
import warnings

# Menonaktifkan peringatan terkait perubahan di masa depan
warnings.simplefilter(action='ignore', category=FutureWarning)

# Mengatur opsi pandas untuk menampilkan peringatan downcasting
pd.set_option('future.no_silent_downcasting', True)

def preprocess_product_data(products_list):
    """
    Fungsi untuk membersihkan dan memproses data produk.
    Mengubah data menjadi DataFrame, membersihkan kolom harga, rating, warna, ukuran, dan jenis kelamin.
    """
    # Mengonversi list produk menjadi DataFrame
    product_df = pd.DataFrame(products_list)
    
    # Menghapus baris yang memiliki judul 'unknown product'
    product_df = product_df[product_df['title'].str.lower() != 'unknown product']
    
    # Membersihkan dan mengonversi harga ke dalam format float dan mengalikan dengan kurs
    product_df['price'] = product_df['price'].replace(r'[^\d.]', '', regex=True)
    product_df['price'] = product_df['price'].replace('', np.nan)
    product_df.dropna(subset=['price'], inplace=True)
    
    # Mengonversi harga menjadi float dan mengalikannya dengan kurs Rupiah
    product_df['price'] = product_df['price'].astype(float) * 16000
    
    # Membersihkan dan mengonversi rating produk
    product_df['rating'] = product_df['rating'].replace(r'[^0-9.]', '', regex=True)
    product_df['rating'] = product_df['rating'].replace('', np.nan)
    product_df.dropna(subset=['rating'], inplace=True)
    
    # Mengonversi rating menjadi tipe data float
    product_df['rating'] = product_df['rating'].astype(float)
    
    # Membersihkan dan mengonversi kolom warna
    product_df['colors'] = product_df['colors'].replace(r'\D', '', regex=True)
    product_df['colors'] = product_df['colors'].replace('', np.nan)
    product_df.dropna(subset=['colors'], inplace=True)
    
    # Mengonversi warna menjadi integer
    product_df['colors'] = product_df['colors'].astype(int)
    
    # Membersihkan kolom ukuran dan jenis kelamin
    product_df['size'] = product_df['size'].replace(r'Size:\s*', '', regex=True)
    product_df['gender'] = product_df['gender'].replace(r'Gender:\s*', '', regex=True)
    
    # Menghapus duplikasi dan nilai null
    product_df.drop_duplicates(inplace=True)
    product_df.dropna(inplace=True)
    
    # Menambahkan kolom timestamp dengan format tanggal dan waktu saat ini
    product_df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return product_df
