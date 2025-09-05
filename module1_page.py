import tkinter as tk
import os
import webbrowser
import win32print  #to remove soon
import win32ui #to remove soon
import sqlite3
import listPort as lp
from tkinter import ttk, messagebox
import printerPopup as pp
class Module1Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.initializeDB()
        self.controller = controller

        # Header
        title = tk.Label(self, text="📦 Module 1: Inventory Management & Label Printing",
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Submodule navigation
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=5)
        # tk.Label(nav_frame, text="supplierNumber:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=2)
        # self.supplierNumber = tk.Entry(nav_frame, width=20)
        # self.supplierNumber.grid(row=0, column=1, sticky="w", padx=(0, 5))
        """
        tk.Button(nav_frame, text="Supplier Management", width=20,
                  command=lambda: self.show_subpage("supplier")).grid(row=0, column=0, padx=5)
        tk.Button(nav_frame, text="Raw Inventory Entry", width=20,
                  command=lambda: self.show_subpage("raw")).grid(row=0, column=1, padx=5)
        tk.Button(nav_frame, text="Final Inventory Entry", width=20,
                  command=lambda: self.show_subpage("final")).grid(row=0, column=2, padx=5)
"""
        # Container for sub-pages
        self.subpages = {}
        self.subpage_container = tk.Frame(self)
        self.subpage_container.pack(fill="both", expand=True)
        self.subpage_container.grid_rowconfigure(0, weight=1)
        self.subpage_container.grid_columnconfigure(0, weight=1)

        for name, FrameClass in {
            "supplier": SupplierManagementPage,
            "raw": RawInventoryEntryPage,
            "final": FinalInventoryEntryPage,
           # "MainMenuPage" : App
        }.items():
            frame = FrameClass(self.subpage_container, controller=self)
            self.subpages[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_subpage("supplier")
        

    def show_subpage(self, name):
        self.subpages[name].tkraise()
        self.subpages[name].grid_rowconfigure(0, weight=1)
        self.subpages[name].grid_columnconfigure(0, weight=1)
        self.subpage_container.grid_rowconfigure(0, weight=1)
        self.subpage_container.grid_columnconfigure(0, weight=1)
    def MainMenu(self):
        self.controller.show_frame("MainMenuPage")
    def initializeDB(self):
        print("Initializing Database...")
        DB_FILE = "inventory.db"
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            supplierCode TEXT PRIMARY KEY,
            supplierName TEXT,
            country TEXT,
            email TEXT,
            contactPerson TEXT,
            contactNumber TEXT,
            facebookPage TEXT,
            webPage TEXT,
            shippingNotes TEXT
            
            
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_inventory (
            supplierCode TEXT PRIMARY KEY,
            supplierName TEXT,
            partNumber TEXT,
            qtyPerMotherBox INTEGER,
            qtyPerInnerBox INTEGER,
            itemDescription TEXT,
            unitOfMeasurement TEXT,
            materialType TEXT,
            color TEXT,
            partCostPerPiece TEXT,
            shelfNumber TEXT,
            shelfLocation TEXT,
            warehouseNumber TEXT,
            warehouseLocation TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS final_inventory (
            customerCode TEXT,
            customerName TEXT,
            partNumber TEXT ,
            qtyPartNumber INTEGER,
            finalItemcode TEXT PRIMARY KEY,
            itemDescription TEXT,
            barcodeNumber TEXT,
            shelfNumber TEXT,
            shelfLocation TEXT,
            warehouseNumber TEXT,
            warehouseLocation TEXT
                       
        )
        """)

        conn.commit()
        conn.close()


        

# ====================
# SUBMODULE A - Supplier Management
# ====================


class SupplierManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.DB_FILE = "inventory.db"
        # top menu bar
        self.menu_panel = tk.Frame(self, bg="#2c3e50", width=00)
        self.menu_panel.pack(side="left", fill="y")

        tk.Button(self.menu_panel, text="Main Menu", bg="#2c3e50", fg="white", font=("Arial", 14, "bold"),command=lambda: self.controller.MainMenu()).pack(pady=10,side="top")
        
        btn_supplier = tk.Button(self.menu_panel, text="Supplier Management", width=20,command=lambda: self.controller.show_subpage("supplier"))
        btn_supplier.pack(pady=5,side="top")

        tk.Button(self.menu_panel, text="Raw Inventory", width=20,command=lambda: self.controller.show_subpage("raw")).pack(pady=5,side="top")
        tk.Button(self.menu_panel, text="Final Inventory", width=20,command=lambda: self.controller.show_subpage("final")).pack(pady=5,side="top")

        # Main Content
        content_frame = tk.Frame(self)
        
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Hide Menu Button
        #btn_close_menu = tk.Button(content_frame, text="❌ Close Menu", command=self.toggle_menu)
       # btn_close_menu.grid(row=0, column=0, sticky="w", columnspan=2)

        # Form Labels and Entries
        form_frame = tk.Frame(content_frame)
        form_frame.grid(row=1, column=0, sticky="nw")

        tk.Label(form_frame, text="supplierNumber:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=2)
        self.supplierNumber = tk.Entry(form_frame, width=50)
        self.supplierNumber.grid(row=0, column=1, sticky="w", padx=(0, 5))

        tk.Label(form_frame, text="supplierName:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=2)
        self.supplierName = tk.Entry(form_frame, width=50)
        self.supplierName.grid(row=1, column=1, sticky="w", padx=(0, 5))

        tk.Label(form_frame, text="country:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", pady=2)
        self.country = tk.Entry(form_frame, width=50)
        self.country.grid(row=2, column=1, sticky="w", padx=(0, 5))

        tk.Label(form_frame, text="email:", font=("Arial", 10)).grid(row=3, column=0, sticky="e", pady=2)
        self.email = tk.Entry(form_frame, width=50)
        self.email.grid(row=3, column=1, sticky="w", padx=(0, 5))

        tk.Label(form_frame, text="Contact Person:", font=("Arial", 10)).grid(row=4, column=0, sticky="e", pady=2)
        self.contact_name = tk.Entry(form_frame, width=50)
        self.contact_name.grid(row=4, column=1, sticky="w", padx=(0, 5))

        tk.Label(form_frame, text="Contact Number:", font=("Arial", 10)).grid(row=5, column=0, sticky="e", pady=2)
        self.contact_number = tk.Entry(form_frame, width=50)
        self.contact_number.grid(row=5, column=1, sticky="w")

        tk.Label(form_frame, text="Facebook Page:", font=("Arial", 10)).grid(row=6, column=0, sticky="e", pady=2)
        self.Facebook = tk.Entry(form_frame, width=50)
        self.Facebook.grid(row=6, column=1, sticky="w")

        tk.Label(form_frame, text="Web Page:", font=("Arial", 10)).grid(row=7, column=0, sticky="e", pady=2)
        self.Web = tk.Entry(form_frame, width=50)
        self.Web.grid(row=7, column=1, sticky="w")

        tk.Label(form_frame, text="Shipping Notes:", font=("Arial", 10)).grid(row=8, column=0, sticky="e", pady=2)
        self.Shipping = tk.Entry(form_frame, width=50)
        self.Shipping.grid(row=8, column=1, sticky="w")
        # Action Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.grid(row=1, column=1, sticky="ne", padx=10)

        actions = [
            ("Add", self.add_supplier),
            ("Edit", self.edit_supplier),
            ("Delete", self.delete_supplier),
            ("Visit Web...", self.openWeb),
        ]
        for label, command in actions:
            tk.Button(button_frame, text=label, width=30, command=command).pack(pady=3)
        content_frame.grid_rowconfigure(2, weight=0)
        content_frame.grid_columnconfigure(0, weight=1)

        # Table Section
        table_frame = tk.Frame(content_frame)
        table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

        columns = (
            "Supplier Number", "Supplier Name", "Country", "Email",
            "Contact Person", "Contact Num.", "FB Page", "Web Page", "Shipping Notes"
        )
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=80,anchor="w")
        
        scroll_x.config(command=self.tree.xview)
        scroll_y.config(command=self.tree.yview)
        self.tree.grid(row=1, column=0, sticky="nsew")
        scroll_y.grid(row=1, column=1, sticky="ns")
        scroll_x.grid(row=2, column=0, sticky="ew")

        # Make the table area resizable
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self.onSelect)

      #  searchFrame = tk.Frame(form_frame)
       # searchFrame.grid(row=10, column=0, sticky="nw")
        tk.Label(form_frame, text=" ").grid(row=10,column=0,sticky="w")
        tk.Label(form_frame, text="Search:").grid(row=11,column=0,sticky="w")
        self.search_entry = tk.Entry(form_frame, width=50)
        self.search_entry.grid(row=11,column=1,sticky="w")
        self.search_entry.bind("<Return>", self.search)
        self.loadSuppliers()
# -------------------------------
# sqlite3 stuff 
# --------------
    def openWeb(self):
        url = self.Web.get().strip()
        if url:
            if not url.startswith("http"):
                url = "http://" + url
            webbrowser.open(url)
        else:
            messagebox.showwarning("No URL", "Web Page field is empty.")
    def search(self,event):
        query = self.search_entry.get().strip()
        self.tree.selection_remove(self.tree.selection())  # clear previous selection
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            sqlcom = """
                SELECT * FROM suppliers
                WHERE supplierCode LIKE ?
                OR supplierName LIKE ?
                OR country LIKE ?
                OR email LIKE ?
                OR contactPerson LIKE ?
                OR contactNumber LIKE ?
                OR facebookPage LIKE ?
                OR webPage LIKE ?
                OR shippingNotes LIKE ?
            """
            params = tuple([f"%{query}%"] * 9)  # 14 fields
            cursor.execute(sqlcom, params)
            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        print("searching..." , query)
    def onSelect(self,event):
        print("dsjofhidsuhfuidh")
        selected_item = self.tree.selection()
        if not selected_item:
            return
        row_values = self.tree.item(selected_item)["values"]
        self.supplierNumber.delete(0, tk.END)
        self.supplierNumber.insert(0, row_values[0])

        self.supplierName.delete(0, tk.END)
        self.supplierName.insert(0, row_values[1])

        self.country.delete(0, tk.END)
        self.country.insert(0, row_values[2])

        self.email.delete(0, tk.END)
        self.email.insert(0, row_values[3])

        self.contact_name.delete(0, tk.END)
        self.contact_name.insert(0, row_values[4])

        self.contact_number.delete(0, tk.END)
        self.contact_number.insert(0, row_values[5])

        self.Facebook.delete(0, tk.END)
        self.Facebook.insert(0, row_values[6])

        self.Web.delete(0, tk.END)
        self.Web.insert(0, row_values[7])

        self.Shipping.delete(0, tk.END)
        self.Shipping.insert(0, row_values[8])       
    def loadSuppliers(self):
        print("Loading Suppliers...")
        self.tree.delete(*self.tree.get_children())
        print(self.DB_FILE)
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM suppliers")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        #self.selected_id = None

    def add_supplier(self):
        data = [
            self.supplierNumber.get(),
            self.supplierName.get(),
            self.country.get(),
            self.email.get(),
            self.contact_name.get(),
            self.contact_number.get(),
            self.Facebook.get(),
            self.Web.get(),
            self.Shipping.get()]
        if not all(field.strip() for field in data):
            messagebox.showwarning("Missing Info", "All fields are required.")
            return
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO suppliers (supplierCode, supplierName, country, email, contactPerson, contactNumber, facebookPage, webPage, shippingNotes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (            
                self.supplierNumber.get(),
                self.supplierName.get(),
                self.country.get(),
                self.email.get(),
                self.contact_name.get(),
                self.contact_number.get(),
                self.Facebook.get(),
                self.Web.get(),
                self.Shipping.get()))
            conn.commit()
        self.loadSuppliers()
    def delete_supplier(self):
        selected = self.tree.selection()
        print(selected)
        if not selected:
            messagebox.showwarning("No selection", "Select a supplier to edit.")
            return
        values = self.tree.item(selected[0], "values")
        supplierCode = values[0]
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM suppliers WHERE supplierCode=?", (supplierCode,))
            conn.commit()
            messagebox.showinfo(supplierCode, "Deleted Successfully")
        self.loadSuppliers()


    def edit_supplier(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a supplier to edit.")
            return
        new_data = [
            self.supplierNumber.get(),
            self.supplierName.get(),
            self.country.get(),
            self.email.get(),
            self.contact_name.get(),
            self.contact_number.get(),
            self.Facebook.get(),
            self.Web.get(),
            self.Shipping.get()
        ]
        if not all(field.strip() for field in new_data):
            messagebox.showwarning("Missing Info", "All fields are required.")
            return
        
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            values = self.tree.item(selected[0], "values")
            original_code = values[0] 
            cursor.execute("SELECT * FROM suppliers WHERE supplierCode=? AND supplierCode<>?", 
                       (self.supplierNumber.get(), original_code))
            if cursor.fetchone() is not None:
                messagebox.showwarning("Error", "Supplier Number already exists")
                return
            cursor.execute("""
                UPDATE suppliers 
                SET supplierCode=?, supplierName=?, country=?, email=?, contactPerson=?, contactNumber=?, facebookPage=?, webPage=?, shippingNotes=?
                WHERE supplierCode=?
            """, (self.supplierNumber.get(),
                self.supplierName.get(),
                self.country.get(),
                self.email.get(),
                self.contact_name.get(),
                self.contact_number.get(),
                self.Facebook.get(),
                self.Web.get(),
                self.Shipping.get(),
                self.supplierNumber.get(),
                ))
            conn.commit()
        self.loadSuppliers()
    

# ====================
# SUBMODULE B - Raw Inventory Entry
# ====================
class RawInventoryEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.DB_FILE = "inventory.db"
        self.controller = controller
        # Side Panel (Main Menu)
        self.menu_panel = tk.Frame(self, bg="#2c3e50", width=200)
        self.menu_panel.pack(side="left", fill="y")

        tk.Button(self.menu_panel, text="Main Menu", bg="#2c3e50", fg="white", font=("Arial", 14, "bold"),command=lambda: self.controller.MainMenu()).pack(pady=10)

        btn_supplier = tk.Button(self.menu_panel, text="Supplier Management", width=20,command=lambda: self.controller.show_subpage("supplier"))
        btn_supplier.pack(pady=5)

        tk.Button(self.menu_panel, text="Raw Inventory", width=20,command=lambda: self.controller.show_subpage("raw")).pack(pady=5)
        tk.Button(self.menu_panel, text="Final Inventory", width=20,command=lambda: self.controller.show_subpage("final")).pack(pady=5)

        # Main content --------
        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=2)
        content_frame.grid_rowconfigure(2, weight=3)
        #tk.Label(content_frame, text="Raw Inventory", font=("Arial", 14, "bold")).grid(pady=10)


        form_frame = tk.LabelFrame(content_frame,text="form entry",padx=10,pady=10)
        form_frame.grid(row=1, column=0, sticky="nsew")
        searchFrame = tk.LabelFrame(content_frame,text="search",padx=10,pady=10)
        searchFrame.grid(row=0, column=0, sticky="nsew")
        tk.Label(searchFrame, text="Search:").grid(row=1,column=0,sticky="w")
        self.search_entry = tk.Entry(searchFrame, width=50)
        self.search_entry.grid(row=1,column=1,sticky="w")
        self.search_entry.bind("<Return>", self.search)

        
        #tk.Button(searchFrame, text="Search", command=self.search).grid(row=1, column=2, sticky="w")

        fields = [
    ("Supplier Code", "supplierCode"),
    ("Supplier Name", "supplierName"),
    ("Part Number", "partNumber"),
    ("Qty per Mother Box", "qtyPerMotherBox"),
    ("Qty per Innerbox ", "qtyPerInnerBox"),
    ("Item Description", "itemDescription"), 
    ("Unit of Measurement", "unitOfMeasurement"),]
        secondField = [
    ("Material Type", "materialType"),
    ("Color", "color"),
    ("Part Cost per Piece", "partCostPerPiece"),
    ("Shelf Number", "shelfNumber"),
    ("Shelf Location", "shelfLocation"),
    ("Warehouse Number", "warehouseNumber"),
    ("Warehouse Location", "warehouseLocation"),
]

        for idx, (label_text, var_name) in enumerate(fields):
            tk.Label(form_frame, text=label_text + ":", font=("Arial", 10)).grid(row=idx  , column=0, sticky="e", pady=2)
            setattr(self, var_name, tk.Entry(form_frame, width=30))
            getattr(self, var_name).grid(row=idx, column=1, sticky="w", padx=(0, 5))
        for idx, (label_text, var_name) in enumerate(secondField):
            tk.Label(form_frame, text=label_text + ":", font=("Arial", 10)).grid(row=idx , column=2, sticky="e", pady=2)
            setattr(self, var_name, tk.Entry(form_frame, width=30))
            getattr(self, var_name).grid(row=idx, column=3, sticky="w", padx=(0, 5))
        table_frame = tk.LabelFrame(content_frame,text="Inventory Table",padx=10,pady=10 )
        table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        self.itemDescription.grid_configure(columnspan=3)
        columns = ( "Supplier Code",
    "Supplier Name",
    "Part Number",
    "Qty Per Mother Box",
    "Qty Per Innerbox Of The Mother Box",
    "Item Description",
    "Unit Of Measurement",
    "Material Type",
    "Color",
    "Part Cost Per Piece",
    "Shelf Number",
    "Shelf Location",
    "Warehouse Number",
    "Warehouse Location")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=50)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.onSelect)
        self.check_var = tk.IntVar() # Variable to store the checkbox state
        self.checkbox = tk.Checkbutton(form_frame, text="Print Label", variable=self.check_var)
        self.checkbox.grid(pady=5,row=4,column=4)
        #tk.Label(form_frame, text="New Raw Inventory Entry").grid(pady=5,row=2,column=4)
        # tk.Button(form_frame, text="Load Selected Column", command=self.onSelect).grid(pady=5,row=2,column=4)
        button_frame = tk.LabelFrame(content_frame,text="",padx=10,pady=10)
        button_frame.grid(row=0, column=1, sticky="nsew", padx=10,rowspan=2)
        content_frame.grid_rowconfigure(2, weight=0)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        tk.Button(button_frame, text="Add", command=self.addRawInv,width=20).pack(expand=True,fill="x",side="top")
        tk.Button(button_frame, text="Edit", command=self.editRawInv,width=20).pack(expand=True,fill="x",side="top")
        tk.Button(button_frame, text="Delete", command=self.deleteRawInv,width=20).pack(expand=True,fill="x",side="top")
        self.loadRawInventory()

#============
#yey its sql now..ihated csv HAWHAWH
#==========
    def search(self,event):
        query = self.search_entry.get().strip()
        print("searching...", query)
        self.tree.selection_remove(self.tree.selection())  # clear previous selection
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            sqlcom = """
                SELECT * FROM raw_inventory
                WHERE supplierCode LIKE ?
                OR supplierName LIKE ?
                OR partNumber LIKE ?
                OR qtyPerMotherBox LIKE ?
                OR qtyPerInnerBox LIKE ?
                OR itemDescription LIKE ?
                OR unitOfMeasurement LIKE ?
                OR materialType LIKE ?
                OR color LIKE ?
                OR partCostPerPiece LIKE ?
                OR shelfNumber LIKE ?
                OR shelfLocation LIKE ?
                OR warehouseNumber LIKE ?
                OR warehouseLocation LIKE ?
            """
            params = tuple([f"%{query}%"] * 14)  # 14 fields
            cursor.execute(sqlcom, params)
            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)


    def onSelect(self,event):
        print("dsjofhidsuhfuidh")
        selected_item = self.tree.selection()
        if not selected_item:
            return
        row_values = self.tree.item(selected_item)["values"]
        self.supplierCode.delete(0, tk.END)
        self.supplierCode.insert(0, row_values[0])

        self.supplierName.delete(0, tk.END)
        self.supplierName.insert(0, row_values[1])

        self.partNumber.delete(0, tk.END)
        self.partNumber.insert(0, row_values[2])

        self.qtyPerMotherBox.delete(0, tk.END)
        self.qtyPerMotherBox.insert(0, row_values[3])

        self.qtyPerInnerBox.delete(0, tk.END)
        self.qtyPerInnerBox.insert(0, row_values[4])

        self.itemDescription.delete(0, tk.END)
        self.itemDescription.insert(0, row_values[5])

        self.unitOfMeasurement.delete(0, tk.END)
        self.unitOfMeasurement.insert(0, row_values[6])

        self.materialType.delete(0, tk.END)
        self.materialType.insert(0, row_values[7])
        
        self.color.delete(0, tk.END)
        self.color.insert(0, row_values[8])
        
        self.partCostPerPiece.delete(0, tk.END)
        self.partCostPerPiece.insert(0, row_values[9])
        
        self.shelfNumber.delete(0, tk.END)
        self.shelfNumber.insert(0, row_values[10])
        
        self.shelfLocation.delete(0, tk.END)
        self.shelfLocation.insert(0, row_values[11])

        self.warehouseNumber.delete(0, tk.END)
        self.warehouseNumber.insert(0, row_values[12])

        self.warehouseLocation.delete(0, tk.END)
        self.warehouseLocation.insert(0, row_values[13])
    def send_to_printer(printer_name, ezpl_code):
        print("Sending to printer:", printer_name)
        """
        Send EZPL raw code directly to a Godex printer.
        """
        # Open the printer
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            # Start a print job
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("EZPL Label", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            
            # Send EZPL bytes
            win32print.WritePrinter(hPrinter, ezpl_code.encode("utf-8"))
            
            # End job
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
      
    def loadRawInventory(self):
        print("Loading Raw Inventory...")
        self.tree.delete(*self.tree.get_children())
        print(self.DB_FILE)
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM raw_inventory")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
    def addRawInv(self):
        print("Adding Raw Inventory...")
        print(self.check_var.get())
        data = [
self.supplierCode.get(),
self.supplierName.get(),
self.partNumber.get(),
self.qtyPerMotherBox.get(),
self.qtyPerInnerBox.get(),
self.itemDescription.get(),
self.unitOfMeasurement.get(),
self.materialType.get(),
self.color.get(),
self.partCostPerPiece.get(),
self.shelfNumber.get(),
self.shelfLocation.get(),
self.warehouseNumber.get(),
self.warehouseLocation.get()

        ]

        if not all(field.strip() for field in data):
            messagebox.showwarning("Missing Info", "All fields are required.")
            return

        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("""
    INSERT INTO raw_inventory (
        supplierCode, supplierName, partNumber,
        qtyPerMotherBox, qtyPerInnerBox, itemDescription,
        unitOfMeasurement, materialType, color,
        partCostPerPiece, shelfNumber, shelfLocation,
        warehouseNumber, warehouseLocation
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (            
self.supplierCode.get(),
self.supplierName.get(),
self.partNumber.get(),
self.qtyPerMotherBox.get(),
self.qtyPerInnerBox.get(),
self.itemDescription.get(),
self.unitOfMeasurement.get(),
self.materialType.get(),
self.color.get(),
self.partCostPerPiece.get(),
self.shelfNumber.get(),
self.shelfLocation.get(),
self.warehouseNumber.get(),
self.warehouseLocation.get()))
            conn.commit()
        self.loadRawInventory()
        if self.check_var.get() == 1:
            print("Checkbox is checked")
            self.print_label(self.itemDescription.get(), self.partNumber.get(), self.qtyPerMotherBox.get(), self.shelfNumber.get(), self.warehouseNumber.get())

        else:
            print("Checkbox is unchecked")
    def print_label(self, item_name, item_code, qty, shelf, warehouse):
        print(item_name, item_code, qty, shelf, warehouse)
        qty_str = self.qtyPerMotherBox.get().strip()  
        try:
            qty = int(qty_str)
        except ValueError:
            messagebox.showerror("Invalid Qty", "Quantity must be a number")
            return

        for i in range(qty):  # Print one label per unit
            ezpl = f"""
    ^Q25,3
    ^W100
    ^H10
    ^P1
    ^S2
    ^AD
    ^C1
    ^R0
    ^L
    A50,30,0,4,1,1,N,"RAW INVENTORY"
    A50,70,0,4,1,1,N,"Item: {item_name}"
    A50,110,0,4,1,1,N,"Code: {item_code}"
    A50,150,0,4,1,1,N,"Qty: 1"
    A50,190,0,4,1,1,N,"Shelf: {shelf}"
    A50,230,0,4,1,1,N,"Warehouse: {warehouse}"
    B50,270,0,1,2,2,50,B,"{item_code}"
    E
    """
            print(f"Generated label {i+1}/{qty}:\n", ezpl)
            printer_name = win32print.GetDefaultPrinter()
            self.send_to_printer(printer_name, ezpl)

        
    def deleteRawInv(self):
        print("Deleting Raw Inventory...")
        selected = self.tree.selection()
        print(selected)
        if not selected:
            messagebox.showwarning("No selection", "No selection made.")
            return
        values = self.tree.item(selected[0], "values")
        partNumber = values[2]
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM raw_inventory WHERE partNumber=?", (partNumber,))
            conn.commit()
            messagebox.showinfo(partNumber, "Deleted Successfully")
        self.loadRawInventory()

    def editRawInv(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "No selection made.")
            return

        new_data = [
self.supplierCode.get(),
self.supplierName.get(),
self.partNumber.get(),
self.qtyPerMotherBox.get(),
self.qtyPerInnerBox.get(),
self.itemDescription.get(),
self.unitOfMeasurement.get(),
self.materialType.get(),
self.color.get(),
self.partCostPerPiece.get(),
self.shelfNumber.get(),
self.shelfLocation.get(),
self.warehouseNumber.get(),
self.warehouseLocation.get()

        ]

        if not all(field.strip() for field in new_data):
            messagebox.showwarning("Missing Info", "All fields are required.")
            return
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()

            # Check if the record already exists (assuming partNumber is the PK)
            cursor.execute("""
                SELECT 1 FROM raw_inventory WHERE partNumber = ?
            """, (self.partNumber.get(),))
            exists = cursor.fetchone()

            if exists:
                # Delete old record
                cursor.execute("""
                    DELETE FROM raw_inventory WHERE partNumber = ?
                """, (self.partNumber.get(),))

            # Insert new record
                cursor.execute("""
                INSERT INTO raw_inventory (
                    supplierCode, supplierName, partNumber,
                    qtyPerMotherBox, qtyPerInnerBox, itemDescription,
                    unitOfMeasurement, materialType, color,
                    partCostPerPiece, shelfNumber, shelfLocation,
                    warehouseNumber, warehouseLocation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.supplierCode.get(),
                self.supplierName.get(),
                self.partNumber.get(),
                self.qtyPerMotherBox.get(),
                self.qtyPerInnerBox.get(),
                self.itemDescription.get(),
                self.unitOfMeasurement.get(),
                self.materialType.get(),
                self.color.get(),
                self.partCostPerPiece.get(),
                self.shelfNumber.get(),
                self.shelfLocation.get(),
                self.warehouseNumber.get(),
                self.warehouseLocation.get()
            ))

                conn.commit()

                messagebox.showinfo("Success", "Raw inventory editedsuccessfully")
            else:
                messagebox.showwarning("Not Found", "Item not found for editing")   
        self.loadRawInventory()
# ====================
# SUBMODULE C - Final Inventory Entry
# ====================
class FinalInventoryEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.DB_FILE = "inventory.db"
        # Side Panel (Main Menu)
        self.menu_panel = tk.Frame(self, bg="#2c3e50", width=200)
        self.menu_panel.pack(side="left", fill="y")

        tk.Button(self.menu_panel, text="Main Menu", bg="#2c3e50", fg="white", font=("Arial", 14, "bold"),command=lambda: self.controller.MainMenu()).pack(pady=10)

        btn_supplier = tk.Button(self.menu_panel, text="Supplier Management", width=20,command=lambda: self.controller.show_subpage("supplier"))
        btn_supplier.pack(pady=5)

        tk.Button(self.menu_panel, text="Raw Inventory", width=20,command=lambda: self.controller.show_subpage("raw")).pack(pady=5)
        tk.Button(self.menu_panel, text="Final Inventory", width=20,command=lambda: self.controller.show_subpage("final")).pack(pady=5)

        # Main content --------
        content_frame = tk.Frame(self)
        content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        # search frame
        searchFrame = tk.LabelFrame(content_frame,text="search",padx=10,pady=10)
        searchFrame.grid(row=0, column=0, sticky="nsew")
        tk.Label(searchFrame, text="Search:").grid(row=1,column=0,sticky="w")
        self.search_entry = tk.Entry(searchFrame, width=50)
        self.search_entry.grid(row=1,column=1,sticky="ew")
        self.search_entry.bind("<Return>", self.searchFinalInv)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(2, weight=3)
        content_frame.grid_rowconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        # tk.Label(content_frame, text="Search Raw Part (Part Number / Shelf / Warehouse):").grid(row=1,column=0,sticky="w")
        #tk.Entry(content_frame, width=50).grid(row=1,column=1,sticky="w")
        form_frame = tk.LabelFrame(content_frame, text="Final Inventory Entry", padx=10, pady=10)
        form_frame.grid(row=1, column=0, sticky="nsew")
        fields = [
    ("Customer Code", "customerCode"),
    ("Customer Name", "customerName"),
    ("Part Numbers Used", "partNumbersUsed"),
    ("Qty of Said Part Number", "qtyOfSaidPartNumber"),
    ("Final Itemcode", "finalItemcode"),
    ("Item Description", "itemDescription"),
    
]
        secondField = [
("Barcode Number", "barcodeNumber"),
    ("Shelf Number", "shelfNumber"),
    ("Shelf Location", "shelfLocation"),
    ("Warehouse Number", "warehouseNumber"),
    ("Warehouse Location", "warehouseLocation"),
]

        for idx, (label_text, var_name) in enumerate(fields):
            tk.Label(form_frame, text=label_text + ":", font=("Arial", 10)).grid(row=idx, column=0, sticky="e", pady=2)
            setattr(self, var_name, tk.Entry(form_frame, width=30))
            getattr(self, var_name).grid(row=idx, column=1, sticky="w", padx=(0, 5))
        for idx, (label_text, var_name) in enumerate(secondField):
            tk.Label(form_frame, text=label_text + ":", font=("Arial", 10)).grid(row=idx, column=2, sticky="e", pady=2)
            setattr(self, var_name, tk.Entry(form_frame, width=30))
            getattr(self, var_name).grid(row=idx, column=3, sticky="w", padx=(0, 5))
        table_frame = tk.LabelFrame(content_frame,text="Final Inventory Table",padx=10,pady=10 )
        table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        self.itemDescription.grid_configure( columnspan=3, sticky="we", padx=(0,5))

        columns = (     "Customer Code",
    "Customer Name",
    "Part Numbers Used",
    "Qty of Said Part Number",
    "Final Itemcode",
    "Item Description",
    "Barcode Number",
    "Shelf Number",
    "Shelf Location",
    "Warehouse Number",
    "Warehouse Location")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=50)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.onSelect)
        #check_var = tk.IntVar() # Variable to store the checkbox state
        # checkbox = tk.Checkbutton(form_frame, text="Print Label", variable=check_var)
        # checkbox.grid(pady=5,row=4,column=4)
        #tk.Label(form_frame, text="New Raw Inventory Entry").grid(pady=5,row=2,column=4)
        

        buttonFrame = tk.LabelFrame(content_frame,text="  ",padx=10,pady=10)
        buttonFrame.grid(row=0, column=1, sticky="nsew ",rowspan=2 ,columnspan=1)
        buttonFrame.grid_columnconfigure(0, weight=1)
        tk.Button(buttonFrame, text="Add",command=self.addFinalInv).grid(pady=5,row=3,column=0, sticky="ew")
        tk.Button(buttonFrame, text="Print to GoDEX Printer", command=pp.choose_port_popup).grid(pady=5,column=0,row=2,sticky="ew")
        tk.Button(buttonFrame, text="Edit",command=self.editFinalinv).grid(pady=5,row=4,column=0, sticky="ew")
        tk.Button(buttonFrame, text="Delete",command=self.deleteFinalInv).grid(pady=5,row=5,column=0, sticky="ew")
        tk.Button(buttonFrame, text="Check Barcode",command=self.checkBarcode).grid(pady=5,column=0, row=1, sticky="ew")
        #tk.Label(buttonFrame, text="Label Preview:").grid(pady=5,column=4, row=6)

        #preview_frame = tk.LabelFrame(buttonFrame, text="30x25mm Label Preview", padx=10, pady=10)
        #preview_frame.grid(pady=10 ,column=4, row=7)
        #tk.Label(preview_frame, text="(Label preview would go here)").grid()

        
     #   tk.Button(form_frame, text="Save to final_inventory").pack()
        self.loadFInalInv()


# ==================
# :p
#==========================
    def searchFinalInv(self,event):
        query = self.search_entry.get().strip()
        self.tree.selection_remove(self.tree.selection())  # clear previous selection
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            sqlcom = """
                SELECT * FROM final_inventory
                WHERE customerCode LIKE ?
                OR customerName LIKE ?
                OR partNumber LIKE ?
                OR qtyPartNumber LIKE ?
                OR finalItemCode LIKE ?
                OR itemDescription LIKE ?
                OR barcodeNumber LIKE ?
                OR shelfNumber LIKE ?
                OR shelfLocation LIKE ?
                OR warehouseNumber LIKE ?
                OR warehouseLocation LIKE ?
            """
            params = tuple([f"%{query}%"] * 11)  # 14 fields
            cursor.execute(sqlcom, params)
            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        print("searching..." , query)
    def onSelect(self,event):
        print("dsjofhidsuhfuidh")
        selected_item = self.tree.selection()
        if not selected_item:
            return
        row_values = self.tree.item(selected_item)["values"]

        self.customerCode.delete(0, tk.END)
        self.customerCode.insert(0, row_values[0])

        self.customerName.delete(0, tk.END)
        self.customerName.insert(0, row_values[1])

        self.partNumbersUsed.delete(0, tk.END)
        self.partNumbersUsed.insert(0, row_values[2])

        self.qtyOfSaidPartNumber.delete(0, tk.END)
        self.qtyOfSaidPartNumber.insert(0, row_values[3])

        self.finalItemcode.delete(0, tk.END)
        self.finalItemcode.insert(0, row_values[4])

        self.itemDescription.delete(0, tk.END)
        self.itemDescription.insert(0, row_values[5])

        self.barcodeNumber.delete(0, tk.END)
        self.barcodeNumber.insert(0, row_values[6])

        self.shelfNumber.delete(0, tk.END)
        self.shelfNumber.insert(0, row_values[7])

        self.shelfLocation.delete(0, tk.END)
        self.shelfLocation.insert(0, row_values[8])

        self.warehouseNumber.delete(0, tk.END)
        self.warehouseNumber.insert(0, row_values[9])

        self.warehouseLocation.delete(0, tk.END)
        self.warehouseLocation.insert(0, row_values[10])     

    def loadFInalInv(self):
        print("Loading Final Inventory...")
        self.tree.delete(*self.tree.get_children())
        #print(self.DB_FILE)
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM final_inventory")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
                #print("Loaded", row)

    def addFinalInv(self):
        print("Adding Final Inventory...")
        data = [
            self.customerCode.get(),
            self.customerName.get(),
            self.partNumbersUsed.get(),
            self.qtyOfSaidPartNumber.get(),
            self.finalItemcode.get(),
            self.itemDescription.get(),
            self.barcodeNumber.get(),
            self.shelfNumber.get(),
            self.shelfLocation.get(),
            self.warehouseNumber.get(),
            self.warehouseLocation.get()
        ]
        if not all(field.strip() for field in data):
            messagebox.showwarning("Missing Info", "All fields are required.")
            return
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("""
    INSERT INTO final_inventory (
        customerCode, customerName, partNumber, qtyPartNumber,
        finalItemcode, itemDescription, barcodeNumber,
        shelfNumber, shelfLocation, warehouseNumber, warehouseLocation
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (            
            self.customerCode.get(),
            self.customerName.get(),
            self.partNumbersUsed.get(),
            self.qtyOfSaidPartNumber.get(),
            self.finalItemcode.get(),
            self.itemDescription.get(),
            self.barcodeNumber.get(),
            self.shelfNumber.get(),
            self.shelfLocation.get(),
            self.warehouseNumber.get(),
            self.warehouseLocation.get()
            ))
            conn.commit()
        self.loadFInalInv()


    def deleteFinalInv(self):
        print("Deleting Final Inventory...")
        selected = self.tree.selection()
        print(selected)
        if not selected:
            messagebox.showwarning("No selection")
            return
        values = self.tree.item(selected[0], "values")
        finalItemcode = values[4]
        #print("deleting", finalItemcode)
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM final_inventory WHERE finalItemcode=?", (finalItemcode,))
            conn.commit()
            messagebox.showinfo(finalItemcode, "Deleted Successfully")
        self.loadFInalInv()

    def editFinalinv(self):
        print("Editing Final Inventory...")
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection")
            return

        new_data = [
            self.customerCode.get(),
            self.customerName.get(),
            self.partNumbersUsed.get(),
            self.qtyOfSaidPartNumber.get(),
            self.finalItemcode.get(),
            self.itemDescription.get(),
            self.barcodeNumber.get(),
            self.shelfNumber.get(),
            self.shelfLocation.get(),
            self.warehouseNumber.get(),
            self.warehouseLocation.get()
        ]

        if not all(field.strip() for field in new_data):
            messagebox.showwarning("Missing Info", "All fields are required.")
            return
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 FROM final_inventory WHERE finalItemcode = ?
            """, (self.finalItemcode.get(),))
            exists = cursor.fetchone()

            if exists:
                # Delete old record
                cursor.execute("""
                    DELETE FROM final_inventory WHERE finalItemcode = ?
                """, (self.finalItemcode.get(),))
                cursor.execute("""
                INSERT INTO final_inventory (
                customerCode,
                customerName,
                partNumber,
                qtyPartNumber,
                finalItemcode,
                itemDescription ,
                barcodeNumber ,
                shelfNumber,
                shelfLocation ,
                warehouseNumber,
                warehouseLocation ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (            self.customerCode.get(),
            self.customerName.get(),
            self.partNumbersUsed.get(),
            self.qtyOfSaidPartNumber.get(),
            self.finalItemcode.get(),
            self.itemDescription.get(),
            self.barcodeNumber.get(),
            self.shelfNumber.get(),
            self.shelfLocation.get(),
            self.warehouseNumber.get(),
            self.warehouseLocation.get()
                ))
                conn.commit()
                messagebox.showinfo("Success", "Final inventory edited successfully")
            else:
                messagebox.showwarning("Error", "Final Itemcode does not exist")
        self.loadFInalInv()
    def print_selected_label_godex(self):
        """Print selected final inventory item to GoDEX printer as 30x25mm label (Barcode, ItemCode, Description)"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select an item to print label.")
            return

        # Get selected row values
        values = self.tree.item(selected[0])["values"]
        itemcode = values[4]
        desc = values[5]
        barcode = values[6]

        # Generate EZPL for 30x25mm label
        ezpl = f"""
^Q100,25
^W240
^H10
^P1
^S2

^L
AY
D11
1911A10020{itemcode}
1911A10050{desc}
1E400100100100{barcode}
E
"""


        try:
            # Send to default printer (Windows only)
            printer_name = win32print.GetDefaultPrinter()

            # Send it
            self.send_to_printer(printer_name, ezpl)            
            messagebox.showinfo("Print", "Label sent to GoDEX printer!")
        except Exception as e:
            messagebox.showerror("Print Error", f"Could not print: {e}")

    

    def send_to_printer(printer_name, ezpl_code):
        """
        Send EZPL raw code directly to a Godex printer.
        """
        # Open the printer
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            # Start a print job
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("EZPL Label", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            
            # Send EZPL bytes
            win32print.WritePrinter(hPrinter, ezpl_code.encode("utf-8"))
            
            # End job
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
    def checkBarcode(self):
        print("Checking Barcode...")
        barcode = self.barcodeInput.get().strip()
        if not barcode:
            messagebox.showwarning("Input Error", "Please enter a barcode number.")
            return
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM final_inventory WHERE barcodeNumber=?", (barcode,))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo("Found", f"Item found:\nItem Code: {result[4]}\nDescription: {result[5]}")
            else:
                messagebox.showwarning("Not Found", "No item found with that barcode.") 