import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

def export_to_csv(dataframe, file_name="products.csv"):
    """
    Ekspor data ke file CSV
    """
    dataframe.to_csv(file_name, index=False)

def update_to_google_sheets(dataframe, spreadsheet_id, range_name):
    """
    Kirim data ke Google Sheets
    """
    # Menggunakan kredensial dari file service account
    creds = Credentials.from_service_account_file('alien-topic-442009-d0-c412e18d7299.json')
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Mengubah DataFrame ke list of lists
    values = dataframe.values.tolist()
    body = {
        'values': values
    }

    # Memperbarui data di Google Sheets
    sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()

def save_to_postgres(dataframe, table_name='products'):
    """
    Simpan data ke database PostgreSQL
    """
    try:
        # Menyiapkan koneksi ke PostgreSQL
        db_username = 'postgres'
        db_password = 'kepo1421'
        db_host = 'localhost'
        db_port = '5432'
        db_name = 'product'

        # Membuat koneksi menggunakan SQLAlchemy untuk PostgreSQL
        engine = create_engine(f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

        # Menyimpan DataFrame ke tabel PostgreSQL, menggantikan data jika tabel sudah ada
        dataframe.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke dalam PostgreSQL '{table_name}'.")

    except Exception as x:
        print(f"Gagal menyimpan ke PostgreSQL: {x}")
