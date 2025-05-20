import unittest
import requests
from unittest.mock import patch, MagicMock
from utils.extract import scrape

class TestExtract(unittest.TestCase):
    @patch('utils.extract.requests.get')
    def test_scrape_success(self, mock_get):
        # Menyiapkan data mock untuk response yang berhasil
        url = "https://fashion-studio.dicoding.dev/"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Test Product</h3>
                    <div class="price-container">$20</div>
                    <p>Rating: 4 stars</p>
                    <p>Colors: Red, Blue</p>
                    <p>Size: S, M, L, XL, XXL</p>
                    <p>Gender: Unisex</p>
                </div>
            </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        # Menjalankan fungsi scrape
        result = scrape(url)
        
        # Menguji hasilnya
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('title', result[0])
        self.assertEqual(result[0]['title'], 'Test Product')
    
    @patch('utils.extract.requests.get')
    def test_scrape_failure(self, mock_get):
        # Menyiapkan mock untuk error koneksi
        url = "https://fashion-studio.dicoding.dev/"
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        
        # Menyiapkan mock untuk error timeout
        url = "https://fashion-studio.dicoding.dev/"
        mock_get.side_effect = requests.exceptions.Timeout("Timeout error")
        
        # Menguji exception jika gagal mengakses URL
        with self.assertRaises(Exception) as context:
            scrape(url)
        self.assertIn('Gagal mengakses URL', str(context.exception))
    
    @patch('utils.extract.requests.get')
    def test_scrape_parsing_error(self, mock_get):
        # Menyiapkan response dengan HTML yang tidak valid
        url = "https://fashion-studio.dicoding.dev/"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Invalid HTML without product cards</body></html>"
        mock_get.return_value = mock_response
        
        # Menguji exception ketika parsing HTML gagal
        with self.assertRaises(Exception) as context:
            scrape(url)
        self.assertIn('Gagal melakukan parsing: Struktur HTML tidak valid atau tidak ditemukan', str(context.exception))

if __name__ == '__main__':
    unittest.main()
