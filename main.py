import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from security.authentication import AuthManager
from security.encryption import EncryptionManager
from database.db_manager import DatabaseManager
from models.password_entry import PasswordEntry
import os

class SecureVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureVault 🔐")
        self.root.geometry("600x450")
        self.root.configure(bg="#1e1e2f")  # Dark background

        self.auth = AuthManager()
        self.db = DatabaseManager()
        self.master_pw = None

        # Style for ttk Treeview
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2e2e3e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#2e2e3e",
                        font=("Arial", 10))
        style.map("Treeview", background=[('selected', '#444466')])

        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#444466", foreground="white")

        # Run login/setup
        if not self.first_time_setup():
            if not self.login():
                self.root.destroy()
                return

        self.encryptor = EncryptionManager(self.master_pw)
        self.create_main_ui()

    # ---------------- AUTH ----------------
    def first_time_setup(self):
        if not self.auth.master_file or not os.path.exists(self.auth.master_file):
            pw = simpledialog.askstring("Setup", "Enter new master password:", show='*')
            if pw:
                self.auth.create_master_password(pw)
                messagebox.showinfo("Success", "Master password created.")
                self.master_pw = pw
                return True
        return False

    def login(self):
        pw = simpledialog.askstring("Login", "Enter master password:", show='*')
        if pw and self.auth.verify_master_password(pw):
            messagebox.showinfo("Success", "Login successful.")
            self.master_pw = pw
            return True
        else:
            messagebox.showerror("Failed", "Login failed. Exiting.")
            return False

    # ---------------- MAIN UI ----------------
    def create_main_ui(self):
        # Header Label
        header = tk.Label(self.root, text="SecureVault 🔐", font=("Arial", 20, "bold"), bg="#1e1e2f", fg="#ffcc00")
        header.pack(pady=15)

        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#1e1e2f")
        btn_frame.pack(pady=10)

        btn_add = tk.Button(btn_frame, text="Add Password", width=18, bg="#ffcc00", fg="#1e1e2f",
                            font=("Arial", 11, "bold"), command=self.add_password_ui)
        btn_add.grid(row=0, column=0, padx=10, pady=5)

        btn_view = tk.Button(btn_frame, text="View Passwords", width=18, bg="#ffcc00", fg="#1e1e2f",
                             font=("Arial", 11, "bold"), command=self.view_passwords_ui)
        btn_view.grid(row=0, column=1, padx=10, pady=5)

        btn_exit = tk.Button(btn_frame, text="Exit", width=18, bg="#ff4444", fg="white",
                             font=("Arial", 11, "bold"), command=self.root.quit)
        btn_exit.grid(row=0, column=2, padx=10, pady=5)

        # Treeview Frame
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=20, fill='both', expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("Website", "Username", "Password"), show='headings')
        self.tree.pack(side='left', fill='both', expand=True)

        # Treeview Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        for col in ("Website", "Username", "Password"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")

    # ---------------- ADD PASSWORD ----------------
    def add_password_ui(self):
        website = simpledialog.askstring("Website", "Enter website:")
        username = simpledialog.askstring("Username", "Enter username:")
        password = simpledialog.askstring("Password", "Enter password:", show='*')
        if website and username and password:
            encrypted_pw = self.encryptor.encrypt(password)
            entry = PasswordEntry(website, username, encrypted_pw)
            self.db.add_entry(entry.website, entry.username, entry.password)
            messagebox.showinfo("Success", "Password stored securely.")
            self.refresh_tree()

    # ---------------- VIEW PASSWORDS ----------------
    def view_passwords_ui(self):
        self.refresh_tree()

    def refresh_tree(self):
        # Clear tree
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Populate
        entries = self.db.get_all_entries()
        for website, username, enc_pw in entries:
            decrypted_pw = self.encryptor.decrypt(enc_pw)
            self.tree.insert("", tk.END, values=(website, username, decrypted_pw))


if __name__ == "__main__":
    root = tk.Tk()
    app = SecureVaultApp(root)
    root.mainloop()