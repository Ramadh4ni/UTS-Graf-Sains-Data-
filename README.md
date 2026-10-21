# UTS-Graf-Sains-Data-
# UTS Graf Sains Data

Yogi Ramadhani 2023B (NIM `23031554198`).

Data interaksi e-commerce [RetailRocket](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset) dimasukkan ke Neo4j sebagai graf Visitor → Item, dibuat representasi vektornya (VSM), dihitung kemiripan antar-item, lalu dipakai untuk rekomendasi dengan KNN. Evaluasinya memakai Hit@5 dan NDCG@5.

Semua analisis dan penjelasan ada di **`UTS_GSD.ipynb`**.

## Isi repositori

```
├── UTS_GSD.ipynb      # notebook utama (poin 3 sampai 2.2)
├── py12.py            # tutorial driver Neo4j (1.2)
├── filter_data.py     # filter data per periode waktu
├── import_data.py     # impor CSV ke Neo4j (1.3)
├── requirements.txt
└── data/events_p1.csv, events_p2.csv
```

## Dataset

Dataset hasil filter tidak diunggah ke GitHub karena ukurannya terlalu besar.
link: [Google Drive](https://drive.google.com/drive/folders/1NL5fXa58kaGCuSJJ1o2Q9ypzarjO8oGJ?usp=sharing)

## Environment

Windows, Python 3.12.10, Neo4j Desktop 2026.09.0, driver `neo4j` 6.4.1, SciPy 1.18.1, scikit-learn 1.9.1, NetworkX 3.7. Database `utsgsd`, koneksi `neo4j://127.0.0.1:7687`.

## Cara menjalankan

**1. Instalasi** (PowerShell, di folder proyek)

```powershell
python -m venv myenv
myenv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Kalau aktivasi diblokir, jalankan sekali `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

**2. Siapkan Neo4j**

Buka Neo4j Desktop, buat instance, buat database `utsgsd`, lalu Start sampai RUNNING.

**3. Filter data** (P1: 2 Jun – 2 Agu 2015 untuk training, P2: 11 – 26 Agu 2015 untuk testing)

```powershell
python filter_data.py --p1-start 2015-06-02 --p1-end 2015-08-02 --p2-start 2015-08-11 --p2-end 2015-08-26
```

**4. Impor P1 ke Neo4j**

```powershell
python import_data.py -p PASSWORD_NEO4J -f events_p1.csv
```

Jangan dijalankan dua kali tanpa mengosongkan database (`MATCH (n) DETACH DELETE n;`), karena relasinya jadi dobel.

**5. Buka notebook**

Buka `UTS_GSD.ipynb` (VS Code dengan kernel `myenv`, atau `jupyter notebook`) dan jalankan sel dari atas ke bawah. Password Neo4j diminta lewat kotak input.

## Hasil singkat

| | |
|---|---|
| Graf (data P1) | 681.413 Visitor, 170.615 Item, 1.316.260 relasi |
| Matriks user × item | 99,9991% kosong, disimpan sebagai matriks sparse |
| Proyeksi terpilih | Item-Item (matriks 16× lebih kecil dari User-User) |
| Similarity | Cosine, top-5 untuk item 89379 ditulis ke graf sebagai `SIMILAR_TO` |
| KNN (k = 5), user 976025 | 3 item iklan: 429769, 459583, 138196 |
| Hit@5 / NDCG@5 | 0 / 0 |

Hit@5 dan NDCG@5 bernilai 0 untuk user ini karena tidak ada rekomendasi yang cocok dengan item di P2. Data sangat sparse (kebanyakan user hanya berinteraksi dengan 1 item) dan ada jeda waktu antara P1 dan P2.

## Catatan

- `requirements.txt` di soal mengunci `neo4j==4.2.1`, tapi versi itu belum punya `execute_query`. Saya pakai driver 6.x. Di driver ini, `routing_` diisi `"r"`, bukan `RoutingControl.READ`.
- Bobot interaksi (view = 1, addtocart = 3, bought = 5) adalah asumsi saya sendiri.
- Semua pemilihan acak memakai seed 42, dan filter waktu memakai UTC.
