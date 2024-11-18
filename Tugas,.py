import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from tkinter import ttk

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    # Membuat koneksi ke database SQLite
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Membuat tabel nilai_siswa jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Kolom ID sebagai primary key
            nama_siswa TEXT,  -- Kolom untuk menyimpan nama siswa
            biologi INTEGER,  -- Kolom untuk menyimpan nilai Biologi
            fisika INTEGER,  -- Kolom untuk menyimpan nilai Fisika
            inggris INTEGER,  -- Kolom untuk menyimpan nilai Inggris
            prediksi_fakultas TEXT  -- Kolom untuk menyimpan prediksi fakultas
        )
    """)
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()
    # Menyisipkan data baru ke tabel
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

# Fungsi untuk mengambil semua data dari tabel
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()
    # Mengambil semua baris dari tabel nilai_siswa
    cursor.execute("SELECT * FROM nilai_siswa")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"  # Biologi tertinggi, prediksi Kedokteran
    elif fisika > biologi and fisika > inggris:
        return "Teknik"  # Fisika tertinggi, prediksi Teknik
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"  # Inggris tertinggi, prediksi Bahasa
    else:
        return "Tidak Diketahui"  # Tidak ada yang dominan

# Fungsi untuk menangani tombol submit
def submit():
    try:
        nama = nama_var.get().strip()  # Mengambil nama dari input
        biologi = int(biologi_var.get())  # Mengambil nilai Biologi
        fisika = int(fisika_var.get())  # Mengambil nilai Fisika
        inggris = int(inggris_var.get())  # Mengambil nilai Inggris

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Simpan ke database
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  # Bersihkan input
        populate_table()  # Perbarui tabel
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk membersihkan input setelah submit
def clear_inputs():
    nama_var.set("")  # Kosongkan input nama
    biologi_var.set("")  # Kosongkan input Biologi
    fisika_var.set("")  # Kosongkan input Fisika
    inggris_var.set("")  # Kosongkan input Inggris

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for item in table.get_children():
        table.delete(item)  # Hapus semua data lama di tabel
    rows = fetch_data()  # Ambil data dari database
    for row in rows:
        table.insert("", "end", values=row)  # Masukkan data ke tabel

# Fungsi untuk memperbarui data yang ada di database
def update_record():
    try:
        selected_item = table.selection()[0]  # Ambil item yang dipilih
        record_id = table.item(selected_item)['values'][0]  # Ambil ID dari item

        # Ambil data dari input
        nama = nama_var.get().strip()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi

        # Update data di database
        conn = sqlite3.connect('nilai_siswa.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE nilai_siswa
            SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
            WHERE id = ?
        """, (nama, biologi, fisika, inggris, prediksi, record_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()  # Bersihkan input
        populate_table()  # Perbarui tabel
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang akan diperbarui.")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk menghapus data dari database
def delete_record():
    try:
        selected_item = table.selection()[0]  # Ambil item yang dipilih
        record_id = table.item(selected_item)['values'][0]  # Ambil ID dari item

        # Hapus data di database
        conn = sqlite3.connect('nilai_siswa.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM nilai_siswa WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        populate_table()  # Perbarui tabel
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang akan dihapus.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk memilih data dari tabel dan mengisinya ke input
def select_record():
    try:
        selected_item = table.selection()[0]  # Ambil item yang dipilih
        record = table.item(selected_item)['values']  # Ambil nilai dari item
        
        # Isi data ke input
        nama_var.set(record[1])
        biologi_var.set(record[2])
        fisika_var.set(record[3])
        inggris_var.set(record[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang ingin diisi.")

# Membuat GUI utama
root = Tk()
root.title("Prediksi Fakultas")

# Variabel untuk input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()

# Label dan Entry untuk input
Label(root, text="Nama Siswa:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol untuk aksi
Button(root, text="Submit", command=submit).grid(row=4, column=0, padx=5, pady=10)
Button(root, text="Update", command=update_record).grid(row=4, column=1, padx=5, pady=10)
Button(root, text="Delete", command=delete_record).grid(row=4, column=2, padx=5, pady=10)

# Tabel untuk menampilkan data
columns = ("ID", "Nama Siswa", "Biologi", "Fisika", "Inggris", "Prediksi Fakultas")
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)  # Atur heading
    table.column(col, width=120)  # Atur lebar kolom
table.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# Inisialisasi database dan tabel
create_database()
populate_table()

# Menjalankan GUI
root.mainloop()
