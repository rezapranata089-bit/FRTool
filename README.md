# FR Tool: Alat Otomatisasi Teks Cerdas untuk Termux

<div align="center">
  <img src="https://files.manuscdn.com/user_upload_by_module/session_file/310519663812152457/FTXeqKjsZGtSOUaZ.jpg" alt="FR Tool Banner" width="100%">
  <br>
  <p>
    <a href="https://github.com/rezapranata089-bit/FRTool"><img src="https://img.shields.io/badge/GITHUB-REPOSITORY-2b2b2b?style=for-the-badge&logo=github" alt="Repository" /></a>
    <a href="https://github.com/rezapranata089-bit/FRTool/issues"><img src="https://img.shields.io/badge/LAPORKAN_BUG-2b2b2b?style=for-the-badge&logo=github" alt="Report Bugs" /></a>
    <a href="#"><img src="https://img.shields.io/badge/TERMUX_SUPPORTED-2b2b2b?style=for-the-badge&logo=termux" alt="Termux" /></a>
  </p>
  <!-- Tombol Clone -->
  <a href="https://github.com/rezapranata089-bit/FRTool">
    <img src="https://img.shields.io/badge/CLONE_FR_TOOL-007EC6?style=for-the-badge&logo=github&logoColor=white" height="50" alt="Clone FR Tool">
  </a>
</div>

## Pengantar

**FR Tool** adalah aplikasi *Find & Replace* cerdas berbasis kecerdasan buatan (AI) yang dirancang untuk lingkungan Termux pada perangkat Android. Aplikasi ini bertujuan untuk menyederhanakan proses pencarian dan penggantian teks yang kompleks, memungkinkan pengguna mengotomatisasi tugas-tugas repetitif dengan efisiensi tinggi.

FR Tool dikembangkan untuk memberikan solusi otomatisasi bagi pengguna Termux, sehingga mereka dapat fokus pada pekerjaan yang lebih strategis, sementara tugas *find & replace* yang memakan waktu ditangani oleh sistem AI.

## Fitur Utama

FR Tool menawarkan serangkaian fitur utama yang dirancang untuk meningkatkan efisiensi dan akurasi dalam operasi *find & replace*:

*   **Pencarian & Penggantian Cerdas:** Memanfaatkan AI untuk identifikasi dan modifikasi teks yang lebih akurat dan efisien, meminimalkan kesalahan dan menghemat waktu.
*   **Dukungan Termux:** Dioptimalkan untuk berjalan lancar di lingkungan Termux Android, memberikan fleksibilitas bagi pengguna perangkat mobile.
*   **Antarmuka Baris Perintah (CLI):** Menyediakan kontrol penuh melalui perintah teks, ideal untuk otomatisasi dan integrasi skrip.
*   **Mode Dry-Run:** Memungkinkan pengguna untuk menguji operasi *find & replace* tanpa membuat perubahan permanen pada file, memastikan keamanan dan akurasi.
*   **Format Patch Fleksibel:** Mendukung berbagai format patch, termasuk format `:find`, `:replace`, dan format `===FIND===/===REPLACE===`.

## Persyaratan Sistem

Untuk menjalankan FR Tool, pastikan Anda memenuhi persyaratan berikut:

*   **Sistem Operasi:** Android
*   **Aplikasi Terminal:** [Termux dari F-Droid](https://f-droid.org/packages/com.termux/) (Sangat direkomendasikan)

> **PENTING:** Gunakan aplikasi **Termux dari F-Droid**. Jangan menggunakan Termux dari Google Play Store karena versi tersebut sudah *deprecated* (usang) dan dapat menyebabkan banyak *error* atau masalah kompatibilitas.

## Instalasi & Penggunaan

Ikuti langkah-langkah di bawah ini secara berurutan pada terminal Termux Anda:

### 1. Perbarui & Tingkatkan Paket Sistem

Pastikan sistem Termux Anda mendapatkan pembaruan paket terbaru untuk menghindari konflik dan memastikan kompatibilitas.

```bash
pkg update && pkg upgrade -y
```

### 2. Instal Git

Git diperlukan untuk mengkloning (mengunduh) repositori FR Tool dari GitHub.

```bash
pkg install git -y
```

### 3. Kloning Repositori

Unduh *source code* FR Tool ke perangkat Anda.

```bash
git clone https://github.com/rezapranata089-bit/FRTool.git
```

### 4. Masuk ke Direktori Proyek

Navigasi ke folder FR Tool yang baru saja diunduh.

```bash
cd FRTool
```

### 5. Berikan Izin Eksekusi

Ubah *permission* file `frpatch` agar dapat dijalankan sebagai program.

```bash
chmod +x frpatch
```

### 6. Jalankan FR Tool

Mulai jalankan alat Find & Replace AI.

```bash
python frpatch.py
```

## Instalasi Cepat (Satu Baris)

Bagi Anda yang menyukai efisiensi, salin dan tempel perintah di bawah ini untuk menginstal dan langsung menjalankan FR Tool dalam satu kali eksekusi:

```bash
pkg update && pkg upgrade -y && pkg install git -y && git clone https://github.com/rezapranata089-bit/FRTool.git && cd FRTool && chmod +x frtool && ./frtool
```

## Tampilan Aplikasi

Berikut adalah beberapa *screenshot* dari FR Tool yang berjalan di Termux:

| Layar Utama | Mode Patch | Contoh Penggunaan Patch |
| :---: | :---: | :---: |
| <img src="https://github.com/rezapranata089-bit/FRTool/raw/master/Tampilan%20tools/Screenshot_20260704_182108_Termux.jpg" width="250"> | <img src="https://github.com/rezapranata089-bit/FRTool/raw/master/Tampilan%20tools/Screenshot_20260704_182116_Termux.jpg" width="250"> | <img src="https://github.com/rezapranata089-bit/FRTool/raw/master/Tampilan%20tools/Screenshot_20260704_182127_Termux.jpg" width="250"> |


## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](https://choosealicense.com/licenses/mit/).

## Kontak & Media Sosial

Jika Anda memiliki pertanyaan, ingin berdiskusi lebih lanjut, atau ingin mengikuti pembaruan terbaru, silakan hubungi pengembang melalui saluran berikut:

| Platform | Tautan |
| :--- | :--- |
| **GitHub Issues** | [Laporkan Masalah di Sini](https://github.com/rezapranata089-bit/FRTool/issues) |
| **TikTok** | [@yfinance3](https://tiktok.com/@yfinance3) |
| **Facebook** | [Zeuxc666](https://m.facebook.com/zeuxc666) |

---

**ZEUXXI** - Juli 2026
