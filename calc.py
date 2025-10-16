import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Koneksi ke database
def koneksi():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Ganti sesuai MySQL kamu
        database="login_db"
    )

# Login
def login():
    user = username_entry.get()
    pw = password_entry.get()
    if not user or not pw:
        messagebox.showwarning("Validasi", "Username dan password wajib diisi.")
        return
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pw))
    result = cursor.fetchone()
    conn.close()
    if result:
        login_frame.pack_forget()
        dashboard_frame.pack()
    else:
        messagebox.showerror("Login Gagal", "Username atau password salah.")

# Tampilkan data user
def tampil_user():
    for i in user_tree.get_children():
        user_tree.delete(i)
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    for row in cursor.fetchall():
        user_tree.insert("", "end", values=row)
    conn.close()

# Tambah atau update user
def simpan_user():
    u = user_entry.get()
    p = pass_entry.get()
    if not u or not p:
        messagebox.showwarning("Validasi", "Isi username dan password.")
        return
    conn = koneksi()
    cursor = conn.cursor()
    if selected_user_id.get() == "":
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (u, p))
        messagebox.showinfo("Sukses", "User ditambahkan.")
    else:
        cursor.execute("UPDATE users SET username=%s, password=%s WHERE id=%s", (u, p, selected_user_id.get()))
        messagebox.showinfo("Sukses", "User diperbarui.")
    conn.commit()
    conn.close()
    tampil_user()
    user_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    selected_user_id.set("")

# Isi form saat klik baris
def isi_form_user(event):
    selected = user_tree.focus()
    if not selected:
        return
    values = user_tree.item(selected)['values']
    selected_user_id.set(values[0])
    user_entry.delete(0, tk.END)
    user_entry.insert(0, values[1])
    pass_entry.delete(0, tk.END)

# Hapus user
def hapus_user():
    selected = user_tree.focus()
    if not selected:
        messagebox.showwarning("Hapus", "Pilih user.")
        return
    id = user_tree.item(selected)['values'][0]
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    tampil_user()
    messagebox.showinfo("Sukses", "User dihapus.")

# GUI
root = tk.Tk()
root.title("Login & Dashboard")
root.geometry("600x500")

selected_user_id = tk.StringVar()

# Login Frame
login_frame = tk.Frame(root, bg="#f0f0f0")
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="Login ke Aplikasi", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

tk.Label(login_frame, text="Username", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
username_entry = tk.Entry(login_frame, font=("Arial", 12))
username_entry.pack(pady=5)

tk.Label(login_frame, text="Password", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
password_entry = tk.Entry(login_frame, show="*", font=("Arial", 12))
password_entry.pack(pady=5)

tk.Button(login_frame, text="Login", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=login).pack(pady=20)




# Dashboard Frame
dashboard_frame = tk.Frame(root)
tk.Button(dashboard_frame, text="Manajemen User", command=lambda: [dashboard_frame.pack_forget(), user_frame.pack(), tampil_user()]).pack(fill="x")
tk.Button(dashboard_frame, text="Logout", command=lambda: [dashboard_frame.pack_forget(), login_frame.pack()]).pack(fill="x")

# User Frame
user_frame = tk.Frame(root)
tk.Label(user_frame, text="Form Tambah / Edit User", font=("Arial", 12, "bold")).pack(pady=5)

tk.Label(user_frame, text="Username").pack()
user_entry = tk.Entry(user_frame)
user_entry.pack()

tk.Label(user_frame, text="Password").pack()
pass_entry = tk.Entry(user_frame, show="*")
pass_entry.pack()

tk.Button(user_frame, text="Simpan", command=simpan_user).pack(pady=5)
tk.Button(user_frame, text="Hapus", command=hapus_user).pack()
tk.Button(user_frame, text="Kembali", command=lambda: [user_frame.pack_forget(), dashboard_frame.pack()]).pack(pady=5)

user_tree = ttk.Treeview(user_frame, columns=("ID", "Username"), show="headings")
user_tree.heading("ID", text="ID")
user_tree.heading("Username", text="Username")
user_tree.pack(fill="x", pady=10)
user_tree.bind("<ButtonRelease-1>", isi_form_user)

root.mainloop()