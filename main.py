from utils.extract import scrape
from utils.transform import preprocess_product_data
from utils.load import export_to_csv, update_to_google_sheets, save_to_postgres

def main():
    base_url = 'https://fashion-studio.dicoding.dev/'
    all_products = []

    # Melakukan scraping pada halaman utama tanpa pagination
    print(f"Mulai scraping halaman utama: {base_url}")
    try:
        products = scrape(base_url)
        all_products.extend(products)
    except Exception as e:
        print(f"Gagal melakukan scraping pada halaman utama: {e}")

    # Melakukan scraping pada halaman 1 hingga 50
    for page in range(1, 51):
        url = f"{base_url}page{page}"
        print(f"Mulai scraping halaman {page}: {url}")
        try:
            products = scrape(url)
            all_products.extend(products)
        except Exception as e:
            print(f"Gagal melakukan scraping pada halaman {page}: {e}")

    # Proses data yang telah diambil
    transformed_data = preprocess_product_data(all_products)
    
    # Menyimpan data ke berbagai format
    export_to_csv(transformed_data)
    save_to_postgres(transformed_data)

    # Update ke Google Sheets
    update_to_google_sheets(
        transformed_data,
        '1Vdmb8X-QFsxJ-nGl1LtY6IDy_m6p6F8cmfUX4ynmB4k',
        'SHEET1!A2'
    )

if __name__ == '__main__':
    main()