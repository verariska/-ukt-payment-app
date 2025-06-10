import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# --- FUNGSI DATABASE ---
def create_connection():
    conn = sqlite3.connect("ukt_payments.db")
    return conn

def setup_database():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nim TEXT,
            nama TEXT,
            invoice TEXT,
            nominal INTEGER,
            metode TEXT,
            tanggal TEXT
        )
    ''')
    conn.commit()
    conn.close()

def simpan_pembayaran(nim, nama, invoice, nominal, metode):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO payments (nim, nama, invoice, nominal, metode, tanggal) VALUES (?, ?, ?, ?, ?, ?)",
              (nim, nama, invoice, nominal, metode, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sukses", "Pembayaran berhasil disimpan!")

def tampilkan_histori():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM payments")
    hasil = c.fetchall()
    conn.close()

    histori_window = tk.Toplevel()
    histori_window.title("Histori Pembayaran")

    header = ["ID", "NIM", "Nama", "Invoice", "Nominal", "Metode", "Tanggal"]
    for j, h in enumerate(header):
        tk.Label(histori_window, text=h, font=('Arial', 10, 'bold'), borderwidth=1, relief="solid", padx=10, pady=5).grid(row=0, column=j, sticky="nsew")

    for i, row in enumerate(hasil):
        for j, value in enumerate(row):
            tk.Label(histori_window, text=value, font=('Arial', 10), borderwidth=1, relief="solid", padx=10, pady=5).grid(row=i+1, column=j, sticky="nsew")

# --- GUI ---
def main_gui():
    setup_database()

    root = tk.Tk()
    root.title("Pembayaran UKT Mahasiswa")
    root.geometry("400x400")
    root.configure(bg="#f4f4f4")

    container = tk.Frame(root, bg="#f4f4f4")
    container.pack(padx=20, pady=20)

    tk.Label(container, text="Form Pembayaran UKT", font=("Helvetica", 16, "bold"), bg="#f4f4f4").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    tk.Label(container, text="NIM:", font=('Arial', 11), bg="#f4f4f4").grid(row=1, column=0, sticky="w")
    entry_nim = tk.Entry(container, width=30)
    entry_nim.grid(row=1, column=1, pady=5)

    tk.Label(container, text="Nama:", font=('Arial', 11), bg="#f4f4f4").grid(row=2, column=0, sticky="w")
    entry_nama = tk.Entry(container, width=30)
    entry_nama.grid(row=2, column=1, pady=5)

    tk.Label(container, text="Nomor Invoice:", font=('Arial', 11), bg="#f4f4f4").grid(row=3, column=0, sticky="w")
    entry_invoice = tk.Entry(container, width=30)
    entry_invoice.grid(row=3, column=1, pady=5)

    tk.Label(container, text="Nominal Pembayaran:", font=('Arial', 11), bg="#f4f4f4").grid(row=4, column=0, sticky="w")
    entry_nominal = tk.Entry(container, width=30)
    entry_nominal.grid(row=4, column=1, pady=5)

    tk.Label(container, text="Metode Pembayaran:", font=('Arial', 11), bg="#f4f4f4").grid(row=5, column=0, sticky="w")
    var_metode = tk.StringVar(container)
    var_metode.set("Transfer Bank")
    metode_dropdown = tk.OptionMenu(container, var_metode, "Virtual Account", "Transfer Bank", "QRIS", "E-Wallet")
    metode_dropdown.config(width=26)
    metode_dropdown.grid(row=5, column=1, pady=5)

    tk.Button(container, text="Bayar Sekarang", bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'),
              command=lambda: simpan_pembayaran(
                  entry_nim.get(),
                  entry_nama.get(),
                  entry_invoice.get(),
                  entry_nominal.get(),
                  var_metode.get()
              )).grid(row=6, column=0, columnspan=2, pady=10)

    tk.Button(container, text="Lihat Histori Pembayaran", bg="#2196F3", fg="white", font=('Arial', 10, 'bold'),
              command=tampilkan_histori).grid(row=7, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
    
    
    
    

