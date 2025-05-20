import unittest
import pandas as pd
from unittest.mock import patch
from utils.transform import preprocess_product_data

class TestTransform(unittest.TestCase):

    def test_transform_data(self):
        # Menyiapkan data produk untuk diuji
        products = [
            {'title': 'Product 10', 'price': '10000', 'rating': '4.0', 'colors': '3', 'size': 'M', 'gender': 'Men'},
            {'title': 'Product 15', 'price': '20000', 'rating': '5.0', 'colors': '5', 'size': 'L', 'gender': 'Women'}
        ]
        
        # Mengubah data produk menjadi DataFrame
        df = preprocess_product_data(products)
        
        # Menguji hasil transformasi data
        self.assertEqual(len(df), 2)  # Memastikan ada 2 produk dalam DataFrame
        self.assertIn('price', df.columns)  # Memastikan kolom 'price' ada
        self.assertIn('rating', df.columns)  # Memastikan kolom 'rating' ada
        self.assertIn('colors', df.columns) # Memastikan kolom 'colors' ada
        self.assertIn('timestamp', df.columns)  # Memastikan kolom 'timestamp' ada
        self.assertTrue(df['price'].iloc[0] > 0)  # Memastikan harga lebih besar dari 0
        self.assertTrue(df['rating'].iloc[0] > 0)  # Memastikan rating lebih besar dari 0
    
    def test_invalid_price(self):
        # Menyiapkan data produk dengan harga tidak valid
        products = [
            {'title': 'Product 10', 'price': 'invalid_price', 'rating': '4.0', 'colors': '3', 'size': 'M', 'gender': 'Men'},
            {'title': 'Product 15', 'price': '20000', 'rating': '5.0', 'colors': 'invalid_colors', 'size': 'L', 'gender': 'Women'}
        ]
        
        # Mengubah data produk menjadi DataFrame
        df = preprocess_product_data(products)
        
        # Menguji hasil ketika harga tidak valid
        self.assertEqual(len(df), 0)  # Tidak ada produk yang valid karena harga tidak valid
    
    def test_main_block(self):
        # Menguji blok '__main__' untuk memastikan semuanya berjalan saat program dijalankan
        with patch.object(unittest, 'main'):
            import tests.test_transform

if __name__ == '__main__':
    unittest.main()
