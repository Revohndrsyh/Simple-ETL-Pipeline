import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import export_to_csv, update_to_google_sheets, save_to_postgres

class TestLoad(unittest.TestCase):

    @patch('utils.load.pd.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        # Menyiapkan data frame untuk diuji
        df = pd.DataFrame({
            'title': ['Product 10', 'Product 15'],
            'price': [10000, 20000],
            'rating': [4.0, 5.0]
        })
        
        # Memanggil fungsi untuk menyimpan data ke CSV
        export_to_csv(df, 'test.csv')
        
        # Menguji apakah fungsi to_csv dipanggil dengan argumen yang benar
        mock_to_csv.assert_called_once_with('test.csv', index=False)
    
    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_save_to_google_sheets(self, mock_creds, mock_build):
        # Menyiapkan data frame untuk diuji
        df = pd.DataFrame({
            'title': ['Product 10', 'Product 15'],
            'price': [10000, 20000],
            'rating': [4.0, 5.0]
        })
        
        # Menyiapkan mock untuk kredensial dan service Google Sheets
        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Memanggil fungsi untuk menyimpan data ke Google Sheets
        update_to_google_sheets(df, 'spreadsheet_id', 'Sheet1!A2')
        
        # Menguji apakah fungsi update dipanggil untuk memperbarui data
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()
    
    @patch('utils.load.create_engine')
    def test_save_to_postgres_success(self, mock_create_engine):
        # Menyiapkan data frame untuk diuji
        df = pd.DataFrame({
            'title': ['Product 10', 'Product 15'],
            'price': [10000, 20000],
            'rating': [4.0, 5.0]
        })
        
        # Menyiapkan mock untuk engine SQLAlchemy
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        # Memanggil fungsi untuk menyimpan data ke PostgreSQL
        with patch('pandas.DataFrame.to_sql') as mock_to_sql:
            save_to_postgres(df)
        
        # Menguji apakah fungsi to_sql dipanggil untuk menyimpan data
        mock_to_sql.assert_called_once()
    
    @patch('utils.load.create_engine')
    def test_save_to_postgres_failure(self, mock_create_engine):
        # Menyiapkan data frame untuk diuji
        df = pd.DataFrame({
            'title': ['Product 10', 'Product 15'],
            'price': [10000, 20000],
            'rating': [4.0, 5.0]
        })
        
        # Menyiapkan mock untuk error koneksi database
        mock_create_engine.side_effect = Exception("Database connection error")
        
        # Menguji apakah pesan error tercetak saat terjadi kegagalan
        with patch('builtins.print') as mock_print:
            save_to_postgres(df)
            self.assertIn("Gagal menyimpan ke PostgreSQL", mock_print.call_args_list[0][0][0])

    # Pengujian untuk data tidak valid yang disimpan ke Google Sheets
    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_invalid_data_to_google_sheets(self, mock_creds, mock_build):
        # Menyiapkan data frame untuk diuji dengan data tidak valid
        df = pd.DataFrame({
            'title': ['Product 10', None],  
            'price': [10000, None],         
            'rating': [4.0, 5.0]
        })
        
        # Menyiapkan mock untuk kredensial dan service Google Sheets
        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Memanggil fungsi untuk menyimpan data ke Google Sheets
        update_to_google_sheets(df, 'spreadsheet_id', 'Sheet1!A2')
        
        # Menguji apakah fungsi update dipanggil untuk memperbarui data
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()

    # Pengujian untuk pengecekan koneksi yang gagal
    @patch('utils.load.create_engine')
    def test_save_to_postgres_invalid_data(self, mock_create_engine):
        # Menyiapkan data frame dengan data tidak valid
        df = pd.DataFrame({
            'title': ['Product 10', None],  
            'price': [10000, None],         
            'rating': [4.0, 5.0]
        })
        
        # Menyiapkan mock untuk koneksi yang gagal
        mock_create_engine.side_effect = Exception("Database connection error")
        
        # Menguji apakah koneksi gagal dan pesan error tercetak
        with patch('builtins.print') as mock_print:
            save_to_postgres(df)
            self.assertIn("Gagal menyimpan ke PostgreSQL", mock_print.call_args_list[0][0][0])

    def test_main_block(self):
        # Menguji blok '__main__' untuk memastikan semuanya berjalan saat program dijalankan
        with patch.object(unittest, 'main'):
            import tests.test_load

if __name__ == '__main__':
    unittest.main()
