import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
# from transform import transform_data, transform_to_DataFrame # Mengimpor fungsi dari modul transform
# from store_to_db import store_to_postgre 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}
 
 
def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        # Memeriksa status kode HTTP
        if response.status_code == 404:
            print(f"Halaman {url} mengembalikan status 404 (Not Found).")
            return None
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None
    
def extract_product_data(product_card):
    # Title
    title_element = product_card.find('h3', class_='product-title')
    title = title_element.text.strip() if title_element else "No title"

    # Price
    price_span = product_card.find('span', class_='price')  # jika harga tersedia
    price_p = product_card.find('p', class_='price')         # jika harga tidak tersedia

    if price_span:
        price = price_span.text.strip()
    elif price_p:
        price = price_p.text.strip()
    else:
        price = "Price Not Found"

    # Detail info: rating, colors, size, gender
    p_tags = product_card.find_all('p', style="font-size: 14px; color: #777;")
    rating = colors = size = gender = None

    for p in p_tags:
        text = p.get_text(strip=True)
        if text.startswith("Rating"):
            rating = text.replace("Rating:", "").strip()
        elif "Colors" in text:
            colors = text.strip()
        elif "Size:" in text:
            size = text.replace("Size:", "").strip()
        elif "Gender:" in text:
            gender = text.replace("Gender:", "").strip()

    return {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender
    }

def scrape_product(base_url, first_page_url, start_page=1, delay=2):
    """Fungsi utama untuk mengambil data produk dari beberapa halaman.
    
    Args:
        base_url: Format URL untuk halaman 2 dan seterusnya
        first_page_url: URL untuk halaman pertama
        start_page: Halaman awal untuk scraping
        delay: Jeda waktu antar requests (detik)
    """
    data = []
    page_number = start_page
 
    while True:
        # Menggunakan URL khusus untuk halaman pertama
        if page_number == 1:
            url = first_page_url
        else:
            url = base_url.format(page_number)
            
        print(f"Scraping halaman: {url}")
 
        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            
            # Cek apakah halaman menunjukkan "Page Not Found" atau "Page not found"
            page_not_found = soup.find_all(text=lambda text: text and ("Page Not Found" in text or "Page not found" in text))
            
            # Cek judul halaman untuk deteksi halaman error
            title_tag = soup.find('h1')
            if title_tag and "Page not found" in title_tag.text:
                print(f"Halaman {url} menampilkan error 'Page not found'. Scraping dihentikan.")
                break
                
            product_cards = soup.find_all('div', class_='product-details')
            
            # Jika tidak ada produk yang ditemukan, kemungkinan halaman tidak valid
            if not product_cards:
                print(f"Tidak ditemukan produk di halaman {url}. Scraping dihentikan.")
                break
                
            for card in product_cards:
                product = extract_product_data(card)
                data.append(product)
 
            next_button = soup.find('li', class_='next')
            if next_button:
                page_number += 1
                time.sleep(delay) # Delay sebelum halaman berikutnya
            else:
                break # Berhenti jika sudah tidak ada next button
        else:
            print(f"Tidak bisa mengakses halaman {url}. Scraping dihentikan.")
            break # Berhenti jika ada kesalahan

    return data

# def main():
#     """Fungsi utama untuk keseluruhan proses scraping, transformasi data, dan penyimpanan."""
#     FIRST_PAGE_URL = 'https://fashion-studio.dicoding.dev/'
#     BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    
#     # Menjalankan scraping untuk mengambil data buku
#     all_product_data = scrape_product(BASE_URL, FIRST_PAGE_URL)
    
#     # # Tampilkan hasilnya
#     # for i, product in enumerate(all_product_data, start=1):
#     #     print(f"Produk #{i}:")
#     #     for key, value in product.items():
#     #         print(f"  {key}: {value}")
#     #     print("-" * 40)
    
#     # # Jika data berhasil diambil, lakukan transformasi dan simpan ke PostgreSQL
#     # if all_books_data:
#     #     try:
#     #         # Mengubah data menjadi DataFrame
#     #         DataFrame = transform_to_DataFrame(all_books_data)
            
#     #         # Mentransformasikan data (misalnya konversi mata uang, rating, dll)
#     #         DataFrame = transform_data(DataFrame, 20000)  # Anggap 20000 adalah nilai tukar yang diperlukan
 
#     #         # Menyimpan data ke PostgreSQL
#     #         db_url = 'postgresql+psycopg2://developer:secretpassword@localhost:5432/booksdb'
#     #         store_to_postgre(DataFrame, db_url)  # Memanggil fungsi untuk menyimpan ke database
 
#     #     except Exception as e:
#     #         print(f"Terjadi kesalahan dalam proses: {e}")
#     # else:
#     #     print("Tidak ada data yang ditemukan.")

# if __name__ == '__main__':
#     main()