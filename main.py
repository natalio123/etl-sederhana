import os
from dotenv import load_dotenv

from utils.extract import scrape_product
from utils.transform import transform_to_DataFrame
from utils.load import store_to_postgre, save_to_csv, save_to_json

def main():
    # Load environment variables dari .env file
    load_dotenv()

    FIRST_PAGE_URL = 'https://fashion-studio.dicoding.dev/'
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'

    print("🔍 Memulai proses scraping data produk...")
    raw_data = scrape_product(BASE_URL, FIRST_PAGE_URL)

    if not raw_data:
        print("Tidak ada data yang berhasil diambil.")
        return

    print(f"{len(raw_data)} produk berhasil diambil.")

    print("Melakukan transformasi data...")
    transformed_df = transform_to_DataFrame(raw_data)

    print("Menyimpan data ke file lokal...")
    save_to_csv(transformed_df, "products.csv")
    save_to_json(transformed_df, "products.json")

    print("Menyimpan data ke PostgreSQL...")
    connection_params = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": int(os.getenv("DB_PORT", 5432))  # fallback default port
    }

    success = store_to_postgre(transformed_df, table_name="products", connection_params=connection_params)

    if success:
        print("✅ Proses ETL selesai dengan sukses.")
    else:
        print("⚠️ Penyimpanan ke database gagal.")

if __name__ == "__main__":
    main()