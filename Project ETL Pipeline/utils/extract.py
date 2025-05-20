import requests
from bs4 import BeautifulSoup

def scrape(url):
    try:
        # Mengirimkan request ke URL dan menangani timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Memeriksa apakah status code 200, jika tidak, raise exception
    except requests.exceptions.RequestException as e:
        raise Exception(f"Gagal mengakses URL: {url}. Detail: {e}")
    
    try:
        # Menggunakan BeautifulSoup untuk parsing HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # Validasi apakah struktur HTML sesuai
        if not soup.find_all('div', class_='collection-card'):
            raise Exception("Struktur HTML tidak valid atau tidak ditemukan")
        
        # Loop untuk mengekstrak data produk dari setiap card
        for card in soup.find_all('div', class_='collection-card'):
            title_tag = card.find('h3', class_='product-title')
            title = title_tag.text.strip() if title_tag else 'No Title'
            
            price_tag = card.find('div', class_='price-container')
            price = price_tag.text.strip() if price_tag else 'No Price'
            
            rating_tag = card.find('p', string=lambda text: text and 'Rating' in text)
            rating = rating_tag.text.strip() if rating_tag else 'No Rating'
            
            colors_tag = card.find('p', string=lambda text: text and 'Colors' in text)
            colors = colors_tag.text.strip() if colors_tag else 'No Color'
            
            size_tag = card.find('p', string=lambda text: text and 'Size' in text)
            size = size_tag.text.strip() if size_tag else 'No Size'
            
            gender_tag = card.find('p', string=lambda text: text and 'Gender' in text)
            gender = gender_tag.text.strip() if gender_tag else 'No Gender'
            
            # Menambahkan produk ke dalam list
            products.append({
                'title': title,
                'price': price,
                'rating': rating,
                'colors': colors,
                'size': size,
                'gender': gender
            })
        
        # Mengecek apakah ada produk yang ditemukan
        if not products:
            raise Exception("Tidak ada produk yang ditemukan")
            
        return products
    
    except Exception as e:
        raise Exception(f"Gagal melakukan parsing: {str(e)}")
