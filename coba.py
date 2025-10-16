import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class ModernLoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistem Manajemen - Login")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        
        # Style configuration
        self.setup_styles()
        
        # Variables
        self.selected_user_id = tk.StringVar()
        self.current_user = None
        
        # Setup frames
        self.setup_login_frame()
        self.setup_dashboard_frame()
        self.setup_user_management_frame()
        
        # Show login frame initially
        self.login_frame.pack(fill="both", expand=True)
        
    def setup_styles(self):
        """Configure modern styles for widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2c3e50',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        
    def create_connection(self):
        """Create database connection with error handling"""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="login",
                autocommit=True
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            return None

    def setup_login_frame(self):
        """Setup modern login frame"""
        self.login_frame = tk.Frame(self.root, bg=self.colors['secondary'])
        
        # Main container
        container = tk.Frame(self.login_frame, bg=self.colors['secondary'])
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Login card
        login_card = tk.Frame(container, bg='white', relief='raised', bd=2)
        login_card.pack(padx=20, pady=20)
        
        # Header
        header = tk.Frame(login_card, bg=self.colors['primary'], height=80)
        header.pack(fill='x', padx=2, pady=2)
        header.pack_propagate(False)
        
        tk.Label(header, text="LOGIN APLIKASI", font=('Arial', 18, 'bold'), 
                bg=self.colors['primary'], fg='white').pack(expand=True)
        
        # Form container
        form_frame = tk.Frame(login_card, bg='white', padx=30, pady=30)
        form_frame.pack(fill='both', expand=True)
        
        # Username field
        tk.Label(form_frame, text="Username", font=('Arial', 11, 'bold'), 
                bg='white', fg=self.colors['dark']).pack(anchor='w', pady=(10, 5))
        
        self.username_entry = tk.Entry(form_frame, font=('Arial', 12), 
                                      relief='solid', bd=1, width=25)
        self.username_entry.pack(fill='x', pady=(0, 15))
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.insert(0, "admin")  # Default value for testing
        
        # Password field
        tk.Label(form_frame, text="Password", font=('Arial', 11, 'bold'), 
                bg='white', fg=self.colors['dark']).pack(anchor='w', pady=(5, 5))
        
        self.password_entry = tk.Entry(form_frame, font=('Arial', 12), 
                                      show="*", relief='solid', bd=1, width=25)
        self.password_entry.pack(fill='x', pady=(0, 20))
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.insert(0, "admin123")  # Default value for testing
        
        # Login button
        login_btn = tk.Button(form_frame, text="MASUK", font=('Arial', 12, 'bold'),
                             bg=self.colors['primary'], fg='white', relief='raised',
                             command=self.login, cursor='hand2', width=20, height=2)
        login_btn.pack(pady=10)
        
        # Test database connection button
        test_db_btn = tk.Button(form_frame, text="Test Koneksi Database", font=('Arial', 9),
                               bg=self.colors['warning'], fg='white', relief='raised',
                               command=self.test_database_connection, cursor='hand2')
        test_db_btn.pack(pady=5)
        
        # Footer
        footer = tk.Frame(login_card, bg=self.colors['light'], height=40)
        footer.pack(fill='x', padx=2, pady=2)
        footer.pack_propagate(False)
        
        tk.Label(footer, text="© 2024 Sistem Manajemen", font=('Arial', 9),
                bg=self.colors['light'], fg=self.colors['dark']).pack(expand=True)

    def setup_dashboard_frame(self):
        """Setup modern dashboard frame"""
        self.dashboard_frame = tk.Frame(self.root, bg=self.colors['light'])
        
        # Header
        header = tk.Frame(self.dashboard_frame, bg=self.colors['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header, bg=self.colors['primary'])
        header_content.pack(expand=True, fill='both', padx=20)
        
        tk.Label(header_content, text="DASHBOARD UTAMA", font=('Arial', 20, 'bold'),
                bg=self.colors['primary'], fg='white').pack(side='left')
        
        # User info on the right
        self.user_info_label = tk.Label(header_content, text="", font=('Arial', 12),
                                       bg=self.colors['primary'], fg='white')
        self.user_info_label.pack(side='right')
        
        # Main content
        content = tk.Frame(self.dashboard_frame, bg=self.colors['light'], padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        # Welcome card
        welcome_card = tk.Frame(content, bg='white', relief='raised', bd=1, padx=20, pady=20)
        welcome_card.pack(fill='x', pady=(0, 20))
        
        self.welcome_label = tk.Label(welcome_card, text="Selamat Datang!", font=('Arial', 16, 'bold'),
                                     bg='white', fg=self.colors['dark'])
        self.welcome_label.pack(pady=10)
        
        tk.Label(welcome_card, text="Silakan pilih menu yang tersedia di bawah ini:",
                font=('Arial', 11), bg='white', fg=self.colors['dark']).pack(pady=(0, 20))
        
        # Menu buttons container
        menu_frame = tk.Frame(content, bg=self.colors['light'])
        menu_frame.pack(fill='both', expand=True)
        
        # Menu buttons
        btn_style = {'font': ('Arial', 12, 'bold'), 'width': 20, 'height': 3, 
                    'cursor': 'hand2', 'relief': 'raised'}
        
        user_btn = tk.Button(menu_frame, text="👥 MANAJEMEN USER", 
                           bg=self.colors['primary'], fg='white',
                           command=self.show_user_management, **btn_style)
        user_btn.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        stats_btn = tk.Button(menu_frame, text="📊 STATISTIK", 
                            bg=self.colors['success'], fg='white',
                            command=self.show_stats, **btn_style)
        stats_btn.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        settings_btn = tk.Button(menu_frame, text="⚙️ PENGATURAN", 
                               bg=self.colors['warning'], fg='white', **btn_style)
        settings_btn.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        logout_btn = tk.Button(menu_frame, text="🚪 LOGOUT", 
                             bg=self.colors['danger'], fg='white',
                             command=self.logout, **btn_style)
        logout_btn.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        
        # Configure grid weights
        menu_frame.columnconfigure(0, weight=1)
        menu_frame.columnconfigure(1, weight=1)
        menu_frame.rowconfigure(0, weight=1)
        menu_frame.rowconfigure(1, weight=1)

    def setup_user_management_frame(self):
        """Setup modern user management frame"""
        self.user_frame = tk.Frame(self.root, bg=self.colors['light'])
        
        # Header
        header = tk.Frame(self.user_frame, bg=self.colors['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="MANAJEMEN USER", font=('Arial', 20, 'bold'),
                bg=self.colors['primary'], fg='white').pack(expand=True)
        
        # Main content
        content = tk.Frame(self.user_frame, bg=self.colors['light'], padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        # Two-column layout
        main_container = tk.Frame(content, bg=self.colors['light'])
        main_container.pack(fill='both', expand=True)
        
        # Left panel - Form
        left_panel = tk.Frame(main_container, bg=self.colors['light'])
        left_panel.pack(side='left', fill='both', padx=(0, 10))
        
        form_card = tk.Frame(left_panel, bg='white', relief='raised', bd=1, padx=20, pady=20)
        form_card.pack(fill='both', pady=(0, 10))
        
        tk.Label(form_card, text="Form Tambah/Edit User", font=('Arial', 14, 'bold'),
                bg='white', fg=self.colors['dark']).pack(anchor='w', pady=(0, 15))
        
        # Username field
        tk.Label(form_card, text="Username *", font=('Arial', 10, 'bold'),
                bg='white', fg=self.colors['dark']).pack(anchor='w', pady=(5, 2))
        
        self.user_entry = tk.Entry(form_card, font=('Arial', 11), relief='solid', bd=1)
        self.user_entry.pack(fill='x', pady=(0, 10))
        
        # Password field
        tk.Label(form_card, text="Password *", font=('Arial', 10, 'bold'),
                bg='white', fg=self.colors['dark']).pack(anchor='w', pady=(5, 2))
        
        self.pass_entry = tk.Entry(form_card, font=('Arial', 11), show="*", 
                                  relief='solid', bd=1)
        self.pass_entry.pack(fill='x', pady=(0, 15))
        
        # Password confirmation
        tk.Label(form_card, text="Konfirmasi Password *", font=('Arial', 10, 'bold'),
                bg='white', fg=self.colors['dark']).pack(anchor='w', pady=(5, 2))
        
        self.pass_confirm_entry = tk.Entry(form_card, font=('Arial', 11), show="*", 
                                          relief='solid', bd=1)
        self.pass_confirm_entry.pack(fill='x', pady=(0, 20))
        
        # Action buttons
        btn_frame = tk.Frame(form_card, bg='white')
        btn_frame.pack(fill='x')
        
        btn_style = {'font': ('Arial', 10, 'bold'), 'width': 10, 'height': 1, 
                    'cursor': 'hand2', 'relief': 'raised'}
        
        tk.Button(btn_frame, text="Simpan", bg=self.colors['success'], fg='white',
                 command=self.simpan_user, **btn_style).pack(side='left', padx=(0, 5))
        
        tk.Button(btn_frame, text="Hapus", bg=self.colors['danger'], fg='white',
                 command=self.hapus_user, **btn_style).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Clear", bg=self.colors['warning'], fg='white',
                 command=self.clear_form, **btn_style).pack(side='left', padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(form_card, text="🔄 Refresh Data", font=('Arial', 9, 'bold'),
                               bg=self.colors['primary'], fg='white', cursor='hand2',
                               command=self.tampil_user)
        refresh_btn.pack(pady=10)
        
        # Right panel - User list
        right_panel = tk.Frame(main_container, bg=self.colors['light'])
        right_panel.pack(side='right', fill='both', expand=True)
        
        list_card = tk.Frame(right_panel, bg='white', relief='raised', bd=1)
        list_card.pack(fill='both', expand=True)
        
        # List header
        list_header = tk.Frame(list_card, bg=self.colors['dark'], height=40)
        list_header.pack(fill='x')
        list_header.pack_propagate(False)
        
        tk.Label(list_header, text="DAFTAR USER", font=('Arial', 12, 'bold'),
                bg=self.colors['dark'], fg='white').pack(expand=True)
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(list_card, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ("ID", "Username", "Tanggal Dibuat")
        self.user_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Tanggal Dibuat", text="Tanggal Dibuat")
        
        self.user_tree.column("ID", width=50, anchor='center')
        self.user_tree.column("Username", width=150)
        self.user_tree.column("Tanggal Dibuat", width=120, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.user_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.user_tree.bind("<<TreeviewSelect>>", self.isi_form_user)
        
        # Back button
        back_btn = tk.Button(right_panel, text="← Kembali ke Dashboard", 
                           font=('Arial', 10, 'bold'), bg=self.colors['primary'], fg='white',
                           command=self.show_dashboard, cursor='hand2', relief='raised')
        back_btn.pack(fill='x', pady=(10, 0))

    def test_database_connection(self):
        """Test database connection"""
        conn = self.create_connection()
        if conn:
            messagebox.showinfo("Koneksi Database", "Koneksi ke database BERHASIL!")
            conn.close()
        else:
            messagebox.showerror("Koneksi Database", 
                               "Gagal terhubung ke database!\n\n"
                               "Pastikan:\n"
                               "1. MySQL server berjalan\n"
                               "2. Database 'login_db' sudah dibuat\n"
                               "3. Username dan password MySQL benar")

    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password harus minimal 6 karakter"
        return True, ""

    def login(self):
        """Handle login process"""
        user = self.username_entry.get().strip()
        pw = self.password_entry.get()
        
        if not user or not pw:
            messagebox.showwarning("Validasi", "Username dan password wajib diisi.")
            return
            
        conn = self.create_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Tidak dapat terhubung ke database!")
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pw))
            result = cursor.fetchone()
            
            if result:
                self.current_user = user
                self.login_frame.pack_forget()
                self.dashboard_frame.pack(fill="both", expand=True)
                self.update_user_info()
                messagebox.showinfo("Login Berhasil", f"Selamat datang, {user}!")
            else:
                messagebox.showerror("Login Gagal", "Username atau password salah.")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Terjadi kesalahan database:\n{err}")
        finally:
            conn.close()

    def update_user_info(self):
        """Update user information in dashboard"""
        if self.current_user:
            self.user_info_label.config(text=f"User: {self.current_user}")
            self.welcome_label.config(text=f"Selamat Datang, {self.current_user}!")

    def tampil_user(self):
        """Display users in treeview"""
        # Clear existing data
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
            
        conn = self.create_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Tidak dapat terhubung ke database!")
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, created_at FROM users ORDER BY id")
            
            users = cursor.fetchall()
            if not users:
                # Insert default admin user if table is empty
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                             ("admin", "admin123"))
                conn.commit()
                cursor.execute("SELECT id, username, created_at FROM users ORDER BY id")
                users = cursor.fetchall()
            
            for row in users:
                # Format date if exists
                created_at = row[2].strftime("%d-%m-%Y %H:%M") if row[2] else "-"
                self.user_tree.insert("", "end", values=(row[0], row[1], created_at))
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Gagal memuat data user:\n{err}")
        finally:
            conn.close()

    def simpan_user(self):
        """Save or update user"""
        u = self.user_entry.get().strip()
        p = self.pass_entry.get()
        p_confirm = self.pass_confirm_entry.get()
        
        if not u or not p:
            messagebox.showwarning("Validasi", "Username dan password wajib diisi.")
            return
            
        if p != p_confirm:
            messagebox.showwarning("Validasi", "Password dan konfirmasi password tidak sama.")
            return
            
        # Validate password strength
        is_valid, msg = self.validate_password(p)
        if not is_valid:
            messagebox.showwarning("Validasi Password", msg)
            return
            
        conn = self.create_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Tidak dapat terhubung ke database!")
            return
            
        try:
            cursor = conn.cursor()
            
            if self.selected_user_id.get() == "":
                # Check if username already exists
                cursor.execute("SELECT id FROM users WHERE username=%s", (u,))
                if cursor.fetchone():
                    messagebox.showwarning("Validasi", "Username sudah terdaftar.")
                    return
                    
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (u, p))
                messagebox.showinfo("Sukses", "User berhasil ditambahkan.")
            else:
                cursor.execute("UPDATE users SET username=%s, password=%s WHERE id=%s", 
                             (u, p, self.selected_user_id.get()))
                messagebox.showinfo("Sukses", "User berhasil diperbarui.")
                
            conn.commit()
            self.tampil_user()
            self.clear_form()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Terjadi kesalahan:\n{err}")
        finally:
            conn.close()

    def isi_form_user(self, event):
        """Fill form when row is clicked"""
        selected = self.user_tree.focus()
        if not selected:
            return
            
        values = self.user_tree.item(selected)['values']
        if values:
            self.selected_user_id.set(values[0])
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, values[1])
            self.pass_entry.delete(0, tk.END)
            self.pass_confirm_entry.delete(0, tk.END)

    def hapus_user(self):
        """Delete selected user"""
        selected = self.user_tree.focus()
        if not selected:
            messagebox.showwarning("Hapus", "Pilih user yang akan dihapus.")
            return
            
        user_id = self.user_tree.item(selected)['values'][0]
        username = self.user_tree.item(selected)['values'][1]
        
        # Prevent deleting current logged in user
        if username == self.current_user:
            messagebox.showwarning("Hapus", "Tidak dapat menghapus user yang sedang login!")
            return
        
        if messagebox.askyesno("Konfirmasi Hapus", 
                             f"Apakah Anda yakin ingin menghapus user '{username}'?"):
            conn = self.create_connection()
            if conn is None:
                messagebox.showerror("Database Error", "Tidak dapat terhubung ke database!")
                return
                
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
                conn.commit()
                
                self.tampil_user()
                self.clear_form()
                messagebox.showinfo("Sukses", "User berhasil dihapus.")
                
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Gagal menghapus user:\n{err}")
            finally:
                conn.close()

    def clear_form(self):
        """Clear the form"""
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.pass_confirm_entry.delete(0, tk.END)
        self.selected_user_id.set("")
        # Clear treeview selection
        for item in self.user_tree.selection():
            self.user_tree.selection_remove(item)

    def show_user_management(self):
        """Show user management frame"""
        self.dashboard_frame.pack_forget()
        self.user_frame.pack(fill="both", expand=True)
        self.tampil_user()

    def show_dashboard(self):
        """Show dashboard frame"""
        self.user_frame.pack_forget()
        self.dashboard_frame.pack(fill="both", expand=True)

    def show_stats(self):
        """Show basic statistics"""
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                
                messagebox.showinfo("Statistik", 
                                  f"Total User Terdaftar: {user_count}\n"
                                  f"User Login Saat Ini: {self.current_user}")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Gagal mengambil statistik:\n{err}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Database Error", "Tidak dapat terhubung ke database!")

    def logout(self):
        """Handle logout"""
        if messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin logout?"):
            self.dashboard_frame.pack_forget()
            self.clear_form()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.current_user = None
            self.login_frame.pack(fill="both", expand=True)

    def run(self):
        """Start the application"""
        self.root.mainloop()

def create_database_and_table():
    """Create database and table if not exists"""
    try:
        # First connect without database to create it
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS login_db")
        cursor.execute("USE login_db")
        
        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if admin user exists, if not create it
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
            print("User admin default dibuat")
        
        conn.commit()
        conn.close()
        print("Database dan tabel berhasil dibuat/diperiksa")
        return True
        
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
        return False

if __name__ == "__main__":
    # Create database and table first
    print("Membuat database dan tabel...")
    if create_database_and_table():
        print("Berhasil membuat database dan tabel!")
        
        # Run application
        app = ModernLoginApp()
        app.run()
    else:
        print("Gagal membuat database dan tabel!")
        messagebox.showerror("Database Error", 
                           "Gagal membuat database dan tabel!\n\n"
                           "Pastikan:\n"
                           "1. MySQL server berjalan\n"
                           "2. User MySQL 'root' tidak memiliki password\n"
                           "3. Anda memiliki hak akses yang cukup")