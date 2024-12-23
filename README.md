# KELAS A, Kelompok 14, Daftar Anggota Team:
1. I0324007, Fidini Tsabita, fidinitsabita
2. I0324012, Julia Nastu Ayuningtyas, julianastu
3. I0324036, Azzah Yumna Nadiva Wibowo, acaaa29

# Library Yang Dibutuhkan
Untuk menjalankan program ini, dibutuhkan library berikut untuk diinstal:  
1. VLC yang digunakan untuk memutar media.  
2. yt-dlp yang digunakan untuk mengunduh video dari YouTube.  
3. Pillow (PIL) yang digunakan untuk pengolahan gambar.

# Tambahan
Selain library-library di atas, font-font (Amertha PERSONAL USE ONLY, Elegante Classica) dan background (canvani4.png, daripin.jpg) juga harus didownload terlebih dahulu agar program bisa berjalan dan tidak error. Berikut link website apabila diperlukan:
1. Amertha PERSONAL USE ONLY, link: https://www.dafont.com/amertha.font
2. Elegante Classica, link: https://www.dafont.com/elegante-classica.font

# Sistem Rekomendasi Musik Berdasarkan Suasana Hati (Mood)
Sebuah kafe menyediakan layanan pemutaran lagu sesuai suasana hati pelanggan. Pelanggan disediakan beberapa pilihan untuk kategori dan suasana hati (mood) yang dirasakan. Aplikasi akan menampilkan daftar lagu yang sesuai dengan pilihan kategori dan mood. Pelanggan diminta memilih satu lagu dari daftar rekomendasi Lagu akan diputar setelahnya.

# Fitur
Fitur yang kami sediakan dalam aplikasi ini:
1. Login Screen
   - Admin Login: Admin bisa masuk menggunakan passcode.
   - Customer Login: Customer hanya memasukkan nama mereka.
2. Admin Interface
   - Menambah mood, genre, lagu, dan link YouTube.
   - Validasi input untuk memastikan semua field terisi.
   - Menghapus mood atau genre yang tidak diperlukan.
   - Melihat daftar lagu yang sudah tersedia.
   - Menghapus daftar lagu yang tidak diperlukan.
   - Tombol Clear All untuk mereset semua input.
3. Customer Interface
   - Memilih mood, genre, dan lagu.
4. Fitur Antrian (Queue)
   - Membuat playlist berdasarkan pilihan customer.
   - Lagu berikutnya akan otomatis diputar setelah lagu selesai.
5. Rekomendasi Musik
   - Sistem memberikan rekomendasi lagu berdasarkan kombinasi mood dan genre yang dipilih customer.
6. Database Sederhana
   - Data lagu, mood, dan genre disimpan dalam file JSON.
7. User Experience
   - Antarmuka desktop yang ramah pengguna 

# Site Map
![sitemap kel 14](https://github.com/user-attachments/assets/d0ab4c1f-7845-42b5-9f22-0a44358669b1)


# Diagram Alir
![flowchart kelompok 14 drawio](https://github.com/user-attachments/assets/f0f739ba-54b2-42af-9cd3-ba0b204e3729)

Dalam diagram alir yang pertama ini, kami belum menambahkan fitur admin sebagai fitur tambahan untuk membuat aplikasi NotaRasa ini menjadi lebih efektif dan efisien digunakan baik untuk admin maupun pelanggan. Selain itu pada flowchart ini, kami masih menggunakan modul webbrowser sebagai pemutar lagu yang sudah ada di listbox sehingga lagu akan diputar di dalam browsernya langsung.

**Revisi Flowchart Kelompok 14**
![Flowchart Kel 14 drawio](https://github.com/user-attachments/assets/5500003c-741f-48b3-99f2-f7cf86084db9)
Diagram alir ini menggambarkan alur aplikasi musik "NotaRasa" yang memungkinkan pengguna memilih dan mendengarkan musik bedasarkan mood yang sedang dirasakan. Sistem dimulai dengan menu utama yang menawarkan dua opsi login: sebagai admin atau pelanggan. Jika pengguna memilih login sebagai admin, mereka akan diminta memasukkan kata sandi. Apabila kata sandi benar, sistem akan membuka antarmuka admin. Dalam antarmuka admin, pengguna memiliki akses untuk mengelola data yang tersimpan dalam sistem, seperti menambahkan data baru atau menghapus data lama. Admin dapat menambahkan mood baru, genre baru, atau lagu baru ke dalam database. Selain itu, admin juga dapat menghapus data mood, genre, atau lagu yang sudah tidak diperlukan, sehingga memastikan data tetap relevan dan terorganisasi.  

Jika pengguna memilih login sebagai pelanggan, mereka harus memasukkan nama, setelah itu sistem akan menampilkan ucapan selamat datang dan menawarkan pilihan berdasarkan mood dan genre. Pelanggan dapat memilih mood dan genre, lalu sistem akan merekomendasikan lagu yang sesuai. Pelanggan dapat memilih lagu yang ingin didengarkan, dan sistem akan memainkannya serta menambahkannya ke dalam antrian. Selanjutnya, pelanggan bisa memilih untuk menambah lebih banyak lagu ke antrian atau keluar dari sistem. Diagram ini menunjukkan alur sistem musik online yang intuitif, memungkinkan interaksi yang fleksibel dan efisien bagi admin maupun pelanggan.
