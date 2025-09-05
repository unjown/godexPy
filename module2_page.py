import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import csv
import os
import sqlite3
import module3_page as m3
class Module2Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.DB_FILE = "inventory.db"
        self.initializeDB()
        self.controller = controller
        # Title and Menu button
        tk.Label(self, text="📃 Module 2: Packing List Creation",
                 font=("Arial", 16, "bold")).pack(pady=10)
        tk.Button(self, text="Main Menu", bg="#2c3e50", fg="white",
                  font=("Arial", 14, "bold"),
                  command=lambda: self.controller.show_frame("MainMenuPage")
                  ).pack(pady=10, anchor='nw')

        # PO Form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="PO Number").grid(row=0, column=0, sticky='e')
        self.POentry = tk.Entry(form_frame)
        self.POentry.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Customer").grid(row=1, column=0, sticky='e')
        self.CustomerEntry = tk.Entry(form_frame)
        self.CustomerEntry.grid(row=1, column=1, padx=5)

        tk.Label(form_frame, text="Date").grid(row=2, column=0, sticky='e')
        self.DateEntry =  tk.Entry(form_frame)
        self.   DateEntry.grid(row=2, column=1, padx=5)

        # Item Selector + Packing List Preview
        container = tk.Frame(self)
        container.pack(pady=10, fill='both', expand=True)

        selector_frame = tk.LabelFrame(container, text="Select Items", padx=10, pady=10)
        selector_frame.pack(side="left", fill="both", expand=True, padx=5)

        preview_frame = tk.LabelFrame(container, text="Packing List Preview", padx=10, pady=10)
        preview_frame.pack(side="right", fill="both", expand=True, padx=5)

        # Treeview for item selection (only show name & code)
        columns = ["Item Code", "Item Name", "Available Qty"]
        self.tree = ttk.Treeview(selector_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)

        tk.Button(selector_frame, text="Add →", command=self.addData).pack(pady=5)

        # Preview table
        self.preview_table = ttk.Treeview(preview_frame,
                                          columns=("ItemCode", "ItemName", "QtyOrdered", "ShelfNumber", "WarehouseNumber","PO","Customer","Date"),
                                          show="headings")
        self.preview_table.heading("ItemCode", text="Code")
        self.preview_table.heading("ItemName", text="Item")
        self.preview_table.heading("QtyOrdered", text="Qty")
        self.preview_table.heading("ShelfNumber", text="Shelf No.")
        self.preview_table.heading("WarehouseNumber", text="Warehouse #")
        self.preview_table.heading("PO", text="PO")
        self.preview_table.heading("Customer", text="Customer")
        self.preview_table.heading("Date", text="Date")

        self.preview_table.column("ItemName", width=120)
        self.preview_table.column("ItemCode", width=50)
        self.preview_table.column("QtyOrdered", width=50)
        self.preview_table.column("ShelfNumber", width=80)
        self.preview_table.column("WarehouseNumber", width=50)
        self.preview_table.column("PO", width=80)
        self.preview_table.column("Customer", width=100)
        self.preview_table.column("Date", width=100)
        self.preview_table.pack(pady=10)
        tk.Button(preview_frame, text="edit" , command=self.editPackingList).pack(pady=5, side="left" ,expand=True,fill='x')
        tk.Button(preview_frame, text="delete" , command=self.deletePackingList).pack(pady=5, side="left",expand=True ,fill='x')
        tk.Button(preview_frame, text="Print Packing List", command=self.print_packing_list_ezpl).pack(side="left", expand=True,fill='x')
        tk.Button(preview_frame, text="Save for assembly", command=self.saveAssembly).pack(side="left", expand=True,fill='x')

        self.loadModule2()
    def saveAssembly(self):
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO packingList SELECT * FROM packingListTemp")
            cursor.execute("DELETE FROM packingListTemp")
            conn.commit()
            print("Saved to packingList and cleared packingListTemp")
            messagebox.showinfo("Saved", "Packing list saved for assembly.")
            self.loadModule2()
            cursor.execute("SELECT * FROM packingList")
            for row in cursor.fetchall():
                print(row)

        
    def loadModule2(self):
        self.tree.delete(*self.tree.get_children())
        self.preview_table.delete(*self.preview_table.get_children())
        print(self.DB_FILE)
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT finalItemcode,itemDescription,qtyPartNumber FROM final_inventory")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            cursor.execute("SELECT * FROM packingListTemp")
            for row in cursor.fetchall():
                self.preview_table.insert("", "end", values=row)

    def addData(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item first.")
            return

        itemCode = self.tree.item(selected[0])['values'][0]
        itemName = self.tree.item(selected[0])['values'][1]
        POEntry = self.POentry.get()
        CustomerEntry = self.CustomerEntry.get()
        DateEntry = self.DateEntry.get()

        qty = simpledialog.askinteger("Quantity Order", "Enter quantity to order:", minvalue=1)
        if qty is None:
            messagebox.showwarning("Cancelled", "No quantity entered.")
            return
        if not POEntry.strip() or not CustomerEntry.strip() or not DateEntry.strip():
            messagebox.showwarning("Cancelled", "Missing PO number or Customer or Date")
            return
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT qtyPartNumber FROM final_inventory WHERE finalItemcode = ?", (itemCode,))
            existing = cursor.fetchone()
            print("existing qty:", existing)
            if existing is None:
                messagebox.showwarning("Cancelled", f"Item code {itemCode} not found in inventory.")
                return
            if existing[0] < qty:
                messagebox.showwarning("Cancelled", f"Not enough stock. Available: {existing[0]}")
                return
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO packingListTemp (ItemName, ItemCode, QtyOrdered, ShelfNumber, WarehouseNumber, PO, Customer, Date)
                SELECT ?, ?, ?, ShelfNumber, WarehouseNumber, ?, ?, ?
                FROM final_inventory
                WHERE finalItemcode = ?
            """, (itemName, itemCode, qty, POEntry, CustomerEntry, DateEntry, itemCode))
            conn.commit()
            #print(cursor.execute("SELECT * FROM packingList").fetchall())
            self.loadModule2()
    def clearPackingList(self):
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE * FROM packingListTemp")
            conn.commit()
            messagebox.showinfo("Cleared", "Packing list Temp cleared.")
        self.initializeDB()
        self.loadModule2()
    def deletePackingList(self):
        selected = self.preview_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item to delete.")
            return
        itemCode = self.preview_table.item(selected[0])['values'][0]
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM packingListTemp WHERE ItemCode = ?", (itemCode,))
            conn.commit()
            messagebox.showinfo("Deleted", f"Item {itemCode} deleted from packing list.")
        self.loadModule2()
    def editPackingList(self):
        selected = self.preview_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item to edit.")
            return
        itemCode = self.preview_table.item(selected[0])['values'][0]
        currentQty = self.preview_table.item(selected[0])['values'][2]

        newQty = simpledialog.askinteger("Edit Quantity", f"Current quantity is {currentQty}. Enter new quantity:", minvalue=1)
        if newQty is None:
            messagebox.showwarning("Cancelled", "No quantity entered.")
            return
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT qtyPartNumber FROM final_inventory WHERE finalItemCode = ?", (itemCode,))
            existing = cursor.fetchone()
            print("existing qty:", existing)
            if existing is None:    
                messagebox.showwarning("Cancelled", f"Item code {itemCode} not found in inventory.")
                return
            if existing[0] < newQty:    
                messagebox.showwarning("Cancelled", f"Not enough stock. Available: {existing[0]}")
                return
        with sqlite3.connect(self.DB_FILE, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE packingListTemp SET QtyOrdered = ? WHERE ItemCode = ?", (newQty, itemCode))
            conn.commit()
            messagebox.showinfo("Updated", f"Quantity for item {itemCode} updated to {newQty}.")
        self.loadModule2()
    def print_packing_list_ezpl(self):
        """Print packing list in EZPL format and send to default printer (Windows only)"""
        ezpl_lines = []
        with open(self.PackingListCSV, "r", newline="") as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader, start=1):
                ezpl_lines.append("^XA")
                ezpl_lines.append(f"^FO50,50^A0N,30,30^FDItem: {row['ItemName']}^FS")
                ezpl_lines.append(f"^FO50,90^A0N,30,30^FDCode: {row['ItemCode']}^FS")
                ezpl_lines.append(f"^FO50,130^A0N,30,30^FDQty: {row['QtyOrdered']}^FS")
                ezpl_lines.append(f"^FO50,170^A0N,30,30^FDShelf: {row['ShelfNumber']}^FS")
                ezpl_lines.append(f"^FO50,210^A0N,30,30^FDWarehouse: {row['WarehouseNumber']}^FS")
                ezpl_lines.append(f"^FO50,250^A0N,30,30^FDPO: {row['PO']}^FS")
                ezpl_lines.append(f"^FO50,290^A0N,30,30^FDCustomer: {row['Customer']}^FS")
                ezpl_lines.append(f"^FO50,330^A0N,30,30^FDDate: {row['Date']}^FS")
                ezpl_lines.append("^XZ")

        ezpl_filename = "packing_list_ezpl.txt"
        with open(ezpl_filename, "w") as ezpl_file:
            ezpl_file.write("\n".join(ezpl_lines))

        try:
            # Send to default printer (Windows only)
            os.startfile(ezpl_filename, "print")
            messagebox.showinfo("Print", "Packing list sent to printer!")
        except Exception as e:
            messagebox.showerror("Print Error", f"Could not print: {e}")
    def initializeDB(self):
        print("Initializing Database(module 2)...")
        DB_FILE = "inventory.db"
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS packingList (
            ItemCode TEXT ,
            itemName TEXT,
            qtyOrdered INTEGER,
            shelfNumber TEXT,
            warehouseNumber TEXT,
            PO TEXT,
            Customer TEXT,
            Date TEXT,
            Status TEXT DEFAULT 'Pending',
            qtyPrepared INTEGER DEFAULT 0
        )
        """)
        print("Initialized packingList table.")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS packingListTemp (
            ItemCode TEXT ,
            itemName TEXT,
            qtyOrdered INTEGER,
            shelfNumber TEXT,
            warehouseNumber TEXT,
            PO TEXT,
            Customer TEXT,
            Date TEXT,
            Status TEXT DEFAULT 'Pending',
            qtyPrepared INTEGER DEFAULT 0
        )
        """)
        print("Initialized packingListTemp table.")
        conn.commit()
        conn.close()
