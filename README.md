<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
</head>
<body>

<h1>ETL Pipeline Project</h1>

<p>Proyek ini merupakan implementasi sederhana dari proses ETL (Extract, Transform, Load) menggunakan Python untuk mengambil data produk dari sumber eksternal, membersihkannya, dan menyimpannya ke dalam database PostgreSQL, file CSV, dan file JSON.</p>

<h2>📁 Struktur Proyek</h2>
<pre>
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── utils/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── main.py
├── submission.txt
├── products.csv
├── products.json
└── requirements.txt
</pre>

<h2>🚀 Cara Menjalankan Script ETL Pipeline</h2>

<ol>
  <li><strong>Clone repositori dan pindah ke folder proyek:</strong>
      <pre><code>git clone https://github.com/natalio123/etl-sederhana.git
cd etl-sederhana</code></pre>
  </li>
  <li><strong>Install semua dependensi:</strong><br>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>

  <li><strong>Setup konfigurasi:</strong>
     <pre><code># Database configuration
DB_HOST=localhost
DB_NAME=product_db
DB_USER=developer
DB_PASSWORD=secretpassword
DB_PORT=5432</code></pre>
  </li>
      
  <li><strong>Jalankan ETL Pipeline:</strong>
    <pre><code>python main.py</code></pre>
  </li>
</ol>
<h3>📤 Output</h3>
<ul>
  <li>File CSV: <code>products.csv</code></li>
  <li>File JSON: <code>products.json</code></li>
  <li>Data dimuat ke PostgreSQL di tabel <code>products</code></li>
</ul>

<h2>🧪 Cara Menjalankan Unit Test</h2>

<p>Unit test telah dibuat untuk setiap komponen ETL pipeline.</p>

<h3>Menjalankan semua unit test</h3>
<pre><code>python -m unittest discover tests</code></pre>

<h3>Menjalankan test spesifik</h3>
<pre><code># Test untuk modul extract
python -m unittest tests/test_extract.py
</code></pre>

<pre><code>#Test untuk modul transform
python -m unittest tests/test_transform.py
</code></pre>

<pre><code>#Test untuk modul load
python -m unittest tests/test_load.py
</code></pre>

<h2>📊 Cara Menjalankan Test Coverage</h2>

<h3>Menjalankan coverage untuk semua unit test</h3>
<pre><code>coverage run -m unittest discover tests</code></pre>

<h3>Menjalankan coverage untuk modul spesifik</h3>
<pre><code># Coverage untuk modul load
coverage run -m unittest tests/test_load.py</code></pre>

<h3>Melihat laporan coverage</h3>
<pre><code>coverage report</code></pre>

<h3>Menghasilkan laporan coverage dalam bentuk HTML</h3>
<pre><code>coverage html</code></pre>
<p>Laporan akan disimpan di folder <code>htmlcov</code>. Buka <code>htmlcov/index.html</code> di browser untuk melihat laporan detail.</p>

<h3>Melihat coverage hanya untuk modul tertentu</h3>
<pre><code>coverage report -m utils/load.py</code></pre>

<hr>
<p><strong>Lisensi:</strong> Proyek ini bebas digunakan untuk tujuan edukasi dan pengembangan pribadi.</p>

</body>
</html>
