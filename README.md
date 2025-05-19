<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
</head>
<body>

  <h1>🧵 Fashion Product ETL Pipeline</h1>
  <p>
    Proyek ini adalah pipeline ETL (Extract, Transform, Load) sederhana untuk mengambil data produk fashion dari situs 
    <a href="https://fashion-studio.dicoding.dev/">Fashion Studio Dicoding</a>, membersihkannya, dan menyimpannya ke database PostgreSQL 
    serta file lokal (CSV dan JSON).
  </p>

  <hr>

  <h2>📁 Struktur Proyek</h2>
  <pre><code>
├── tests/                     # Unit tests
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── utils/                     # Modul ETL
│   ├── extract.py             # Fungsi scraping data
│   ├── transform.py           # Fungsi pembersihan & transformasi data
│   └── load.py                # Fungsi penyimpanan data
├── main.py                    # Entry point program ETL
├── requirements.txt           # Daftar dependensi Python
└── README.md                  # Dokumentasi proyek
  </code></pre>

  <hr>

  <h2>🚀 Cara Menjalankan</h2>
  <ol>
    <li><strong>Clone repositori dan pindah ke folder proyek:</strong>
      <pre><code>git clone https://github.com/username/etl-sederhana.git
cd etl-sederhana</code></pre>
    </li>
    <li><strong>Install dependencies:</strong>
      <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li><strong>Jalankan pipeline:</strong>
      <pre><code>python main.py</code></pre>
    </li>
  </ol>

  <hr>

  <h2>⚙️ Konfigurasi Database</h2>
  <p>Pastikan PostgreSQL sudah berjalan dan database <code>product_db</code> sudah dibuat.</p>
  <p>Contoh <code>connection_params</code> yang digunakan:</p>
  <pre><code>{
    "host": "localhost",
    "database": "product_db",
    "user": "developer",
    "password": "secretpassword",
    "port": 5432
}</code></pre>

  <hr>

  <h2>🧪 Testing</h2>
  <p>Untuk menjalankan unit test:</p>
  <pre><code>python -m unittest tests//</code></pre>

  <hr>

  <h2>📦 Output</h2>
  <ul>
    <li><code>products.csv</code> → Data produk dalam format CSV</li>
    <li>Data juga akan disimpan ke tabel <code>products</code> di PostgreSQL</li>
  </ul>

  <hr>

  <h2>📌 Catatan</h2>
  <ul>
    <li>Nilai tukar USD ke IDR digunakan sebesar <strong>16.000</strong></li>
    <li>Produk dengan nilai invalid seperti <code>No title</code> atau <code>Price Unavailable</code> akan disaring atau dibersihkan saat transformasi</li>
    <li><code>google-sheets-api.json</code> belum digunakan, tapi disiapkan untuk fitur ekspor ke Google Sheets di masa depan</li>
  </ul>

  <hr>

  <h2>📄 Lisensi</h2>
  <p>Proyek ini bersifat open-source. Bebas digunakan untuk belajar dan pengembangan.</p>

</body>
</html>
