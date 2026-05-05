import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "mdtarikkhan0786",
}
DB_NAME = "supplychaindb"

# ---------- Database Functions ----------

def initialize_db():
    """Initializes the database and tables if they do not exist."""
    try:
        # First connect without database to create it if missing
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        
        # Create Suppliers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Suppliers (
                SupplierID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                ContactInfo TEXT,
                Rating INT DEFAULT 0
            )
        """)
        
        # Create Products Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                ProductID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                SupplierID INT,
                Stock INT DEFAULT 0,
                WarehouseID INT,
                FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID) ON DELETE SET NULL
            )
        """)
        
        conn.commit()
        conn.close()
    except Error as e:
        messagebox.showerror("Database Error", f"Error during database initialization: {e}")

def connect_db():
    """Returns a connection to the supplychaindb database."""
    return mysql.connector.connect(
        **DB_CONFIG,
        database=DB_NAME
    )

# ---------- Supplier CRUD Functions ----------

def load_suppliers():
    try:
        supplier_tree.delete(*supplier_tree.get_children())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Suppliers")
        for row in cursor.fetchall():
            supplier_tree.insert("", tk.END, values=row)
        conn.close()
    except Error as e:
        messagebox.showerror("Database Error", f"Could not load suppliers: {e}")

def add_supplier():
    name = supplier_name.get()
    contact = supplier_contact.get()
    rating = supplier_rating.get()
    if not name or not contact or not rating:
        messagebox.showerror("Input Error", "All fields are required.")
        return
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Suppliers (Name, ContactInfo, Rating) VALUES (%s, %s, %s)",
                       (name, contact, rating))
        conn.commit()
        conn.close()
        load_suppliers()
        clear_supplier_fields()
        messagebox.showinfo("Success", "Supplier added successfully!")
    except Error as e:
        messagebox.showerror("Database Error", f"Could not add supplier: {e}")

def edit_supplier():
    selected = supplier_tree.selection()
    if not selected:
        messagebox.showwarning("Select Row", "Please select a supplier to edit from the list.")
        return
    item = supplier_tree.item(selected)
    supplier_id = item["values"][0]
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE Suppliers SET Name=%s, ContactInfo=%s, Rating=%s WHERE SupplierID=%s",
                       (supplier_name.get(), supplier_contact.get(), supplier_rating.get(), supplier_id))
        conn.commit()
        conn.close()
        load_suppliers()
        messagebox.showinfo("Success", "Supplier updated successfully!")
    except Error as e:
        messagebox.showerror("Database Error", f"Could not update supplier: {e}")

def delete_supplier():
    selected = supplier_tree.selection()
    if not selected:
        messagebox.showwarning("Select Row", "Please select a supplier to delete.")
        return
    
    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this supplier?"):
        return

    supplier_id = supplier_tree.item(selected)["values"][0]
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Suppliers WHERE SupplierID = %s", (supplier_id,))
        conn.commit()
        conn.close()
        load_suppliers()
        clear_supplier_fields()
        messagebox.showinfo("Success", "Supplier deleted successfully!")
    except Error as e:
        messagebox.showerror("Database Error", f"Could not delete supplier: {e}")

def fill_supplier_fields(event):
    selected = supplier_tree.selection()
    if selected:
        values = supplier_tree.item(selected)["values"]
        supplier_name.set(values[1])
        supplier_contact.set(values[2])
        supplier_rating.set(values[3])

def clear_supplier_fields():
    supplier_name.set("")
    supplier_contact.set("")
    supplier_rating.set("")

# ---------- Product CRUD Functions ----------

def load_products():
    try:
        product_tree.delete(*product_tree.get_children())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        for row in cursor.fetchall():
            product_tree.insert("", tk.END, values=row)
        conn.close()
    except Error as e:
        messagebox.showerror("Database Error", f"Could not load products: {e}")

def add_product():
    name = product_name.get()
    supplier_id = product_supplier_id.get()
    stock = product_stock.get()
    warehouse_id = product_warehouse_id.get()
    if not name or not supplier_id or not stock or not warehouse_id:
        messagebox.showerror("Input Error", "All fields are required.")
        return
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (Name, SupplierID, Stock, WarehouseID) VALUES (%s, %s, %s, %s)",
                       (name, supplier_id, stock, warehouse_id))
        conn.commit()
        conn.close()
        load_products()
        clear_product_fields()
        messagebox.showinfo("Success", "Product added successfully!")
    except Error as e:
        messagebox.showerror("Database Error", f"Could not add product: {e}")

def edit_product():
    selected = product_tree.selection()
    if not selected:
        messagebox.showwarning("Select Row", "Please select a product to edit from the list.")
        return
    product_id = product_tree.item(selected)["values"][0]
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE Products SET Name=%s, SupplierID=%s, Stock=%s, WarehouseID=%s WHERE ProductID=%s",
                       (product_name.get(), product_supplier_id.get(), product_stock.get(), product_warehouse_id.get(), product_id))
        conn.commit()
        conn.close()
        load_products()
        messagebox.showinfo("Success", "Product updated successfully!")
    except Error as e:
        messagebox.showerror("Database Error", f"Could not update product: {e}")

def delete_product():
    selected = product_tree.selection()
    if not selected:
        messagebox.showwarning("Select Row", "Please select a product to delete.")
        return

    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
        return

    product_id = product_tree.item(selected)["values"][0]
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Products WHERE ProductID = %s", (product_id,))
        conn.commit()
        conn.close()
        load_products()
        clear_product_fields()
        messagebox.showinfo("Success", "Product deleted successfully!")
    except Error as e:
        messagebox.showerror("Database Error", f"Could not delete product: {e}")

def fill_product_fields(event):
    selected = product_tree.selection()
    if selected:
        values = product_tree.item(selected)["values"]
        product_name.set(values[1])
        product_supplier_id.set(values[2])
        product_stock.set(values[3])
        product_warehouse_id.set(values[4])

def clear_product_fields():
    product_name.set("")
    product_supplier_id.set("")
    product_stock.set("")
    product_warehouse_id.set("")

# ---------- GUI Setup ----------

root = tk.Tk()
root.title("Supply Chain Admin - Premium Panel")
root.geometry("1000x700")
root.configure(bg="#121212")

# Custom Styles
style = ttk.Style()
style.theme_use('clam')

# Colors
BG_COLOR = "#121212"
CARD_BG = "#1e1e1e"
ACCENT_COLOR = "#0078d4"
TEXT_COLOR = "#e0e0e0"

style.configure("TFrame", background=BG_COLOR)
style.configure("Card.TFrame", background=CARD_BG, relief="flat")
style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
style.configure("Card.TLabel", background=CARD_BG, foreground=TEXT_COLOR, font=("Segoe UI", 10))
style.configure("Header.TLabel", background=BG_COLOR, foreground=ACCENT_COLOR, font=("Segoe UI", 18, "bold"))

style.configure("TButton", 
                background=ACCENT_COLOR, 
                foreground="white", 
                borderwidth=0, 
                focuscolor=ACCENT_COLOR, 
                font=("Segoe UI", 10, "bold"),
                padding=5)
style.map("TButton", 
          background=[('active', '#005a9e'), ('pressed', '#004275')])

style.configure("TEntry", fieldbackground="#2d2d2d", foreground="white", borderwidth=0)

style.configure("Treeview", 
                background="#2d2d2d", 
                foreground=TEXT_COLOR, 
                fieldbackground="#2d2d2d", 
                rowheight=30, 
                font=("Segoe UI", 10))
style.configure("Treeview.Heading", 
                background="#333333", 
                foreground="white", 
                relief="flat", 
                font=("Segoe UI", 10, "bold"))
style.map("Treeview", background=[('selected', ACCENT_COLOR)])

style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
style.configure("TNotebook.Tab", 
                background="#333333", 
                foreground="white", 
                padding=[15, 5], 
                font=("Segoe UI", 10, "bold"))
style.map("TNotebook.Tab", 
          background=[('selected', ACCENT_COLOR)],
          foreground=[('selected', 'white')])

# Main Layout
header_frame = ttk.Frame(root)
header_frame.pack(fill="x", padx=20, pady=20)
ttk.Label(header_frame, text="Supply Chain Management System", style="Header.TLabel").pack(side="left")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# ---------- Supplier Tab ----------
supplier_tab = ttk.Frame(notebook)
notebook.add(supplier_tab, text="  Suppliers  ")

# Supplier Form
sup_form_frame = ttk.Frame(supplier_tab, style="Card.TFrame")
sup_form_frame.pack(side="left", fill="y", padx=10, pady=10)

ttk.Label(sup_form_frame, text="Supplier Details", style="Card.TLabel", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

supplier_name = tk.StringVar()
supplier_contact = tk.StringVar()
supplier_rating = tk.StringVar()

ttk.Label(sup_form_frame, text="Name:", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=5)
ttk.Entry(sup_form_frame, textvariable=supplier_name, width=25).grid(row=1, column=1, pady=5, padx=5)

ttk.Label(sup_form_frame, text="Contact Info:", style="Card.TLabel").grid(row=2, column=0, sticky="nw", pady=5)
# Using a Text box would be better for multi-line but keeping it simple for now as Entry was used
ttk.Entry(sup_form_frame, textvariable=supplier_contact, width=25).grid(row=2, column=1, pady=5, padx=5)

ttk.Label(sup_form_frame, text="Rating (1-5):", style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=5)
ttk.Entry(sup_form_frame, textvariable=supplier_rating, width=25).grid(row=3, column=1, pady=5, padx=5)

btn_frame = ttk.Frame(sup_form_frame, style="Card.TFrame")
btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

ttk.Button(btn_frame, text="Add Supplier", command=add_supplier).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Update", command=edit_supplier).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="Delete", command=delete_supplier).grid(row=1, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

# Supplier Table
sup_list_frame = ttk.Frame(supplier_tab)
sup_list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

supplier_tree = ttk.Treeview(sup_list_frame, columns=("ID", "Name", "Contact", "Rating"), show="headings")
supplier_tree.heading("ID", text="ID")
supplier_tree.heading("Name", text="Supplier Name")
supplier_tree.heading("Contact", text="Contact Info")
supplier_tree.heading("Rating", text="Rating")

supplier_tree.column("ID", width=50, anchor="center")
supplier_tree.column("Rating", width=80, anchor="center")

supplier_tree.pack(fill="both", expand=True)
supplier_tree.bind("<<TreeviewSelect>>", fill_supplier_fields)

# ---------- Product Tab ----------
product_tab = ttk.Frame(notebook)
notebook.add(product_tab, text="  Products  ")

# Product Form
prod_form_frame = ttk.Frame(product_tab, style="Card.TFrame")
prod_form_frame.pack(side="left", fill="y", padx=10, pady=10)

ttk.Label(prod_form_frame, text="Product Details", style="Card.TLabel", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

product_name = tk.StringVar()
product_supplier_id = tk.StringVar()
product_stock = tk.StringVar()
product_warehouse_id = tk.StringVar()

ttk.Label(prod_form_frame, text="Product Name:", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=5)
ttk.Entry(prod_form_frame, textvariable=product_name, width=25).grid(row=1, column=1, pady=5, padx=5)

ttk.Label(prod_form_frame, text="Supplier ID:", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=5)
ttk.Entry(prod_form_frame, textvariable=product_supplier_id, width=25).grid(row=2, column=1, pady=5, padx=5)

ttk.Label(prod_form_frame, text="Current Stock:", style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=5)
ttk.Entry(prod_form_frame, textvariable=product_stock, width=25).grid(row=3, column=1, pady=5, padx=5)

ttk.Label(prod_form_frame, text="Warehouse ID:", style="Card.TLabel").grid(row=4, column=0, sticky="w", pady=5)
ttk.Entry(prod_form_frame, textvariable=product_warehouse_id, width=25).grid(row=4, column=1, pady=5, padx=5)

p_btn_frame = ttk.Frame(prod_form_frame, style="Card.TFrame")
p_btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

ttk.Button(p_btn_frame, text="Add Product", command=add_product).grid(row=0, column=0, padx=5)
ttk.Button(p_btn_frame, text="Update", command=edit_product).grid(row=0, column=1, padx=5)
ttk.Button(p_btn_frame, text="Delete", command=delete_product).grid(row=1, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

# Product Table
prod_list_frame = ttk.Frame(product_tab)
prod_list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

product_tree = ttk.Treeview(prod_list_frame, columns=("ID", "Name", "SupplierID", "Stock", "WarehouseID"), show="headings")
product_tree.heading("ID", text="ID")
product_tree.heading("Name", text="Product Name")
product_tree.heading("SupplierID", text="Supplier ID")
product_tree.heading("Stock", text="Stock")
product_tree.heading("WarehouseID", text="Warehouse ID")

product_tree.column("ID", width=50, anchor="center")
product_tree.column("SupplierID", width=100, anchor="center")
product_tree.column("Stock", width=80, anchor="center")
product_tree.column("WarehouseID", width=100, anchor="center")

product_tree.pack(fill="both", expand=True)
product_tree.bind("<<TreeviewSelect>>", fill_product_fields)

# ---------- Initialization ----------

if __name__ == "__main__":
    # Initialize DB and Tables
    initialize_db()
    
    # Load Initial Data
    load_suppliers()
    load_products()
    
    root.mainloop()
