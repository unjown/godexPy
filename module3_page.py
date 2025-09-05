import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import sqlite3


# ??? orderTable and table are reversed??? also how is the autocomplete really good wth 
class Module3Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.scanned_code = ""
        tk.Label(self, text="🛠️ Module 3: Product Assembly Validation",
                 font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self, text="Main Menu", bg="#2c3e50", fg="white",
                  font=("Arial", 14, "bold"),
                  command=lambda: self.controller.show_frame("MainMenuPage")
                  ).pack(pady=10, anchor='nw')
        # Table of items to validate
        container = tk.Frame(self)
        container.pack(pady=10, fill='both', expand=True)

        tableFrame = tk.LabelFrame(container, text="Select Items", padx=10, pady=10)
        tableFrame.pack(side="right", fill="both", expand=True, padx=5)

        orderTableFrame = tk.LabelFrame(container, text="Packing List Preview", padx=10, pady=10)
        orderTableFrame.pack(side="left", fill="both", expand=True, padx=5)

        self.table = ttk.Treeview(
            tableFrame,   
            columns=("ItemName", "ItemCode", "QtyOrdered", "ShelfNumber", "WarehouseNumber" ,"PO","Customer","Date","Status"),
            show="headings"
        )

        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=80)

        self.table.grid(pady=10, row=0, column=0, sticky="nsew")

        self.orderTable = ttk.Treeview(
            orderTableFrame,   
            columns=("customer"),
            show="headings"
        )

        for col in self.orderTable["columns"]:
            self.orderTable.heading(col, text=col)
            self.orderTable.column(col, width=80)
        self.orderTable.grid(pady=10, sticky="nsew", row=0, column=0)

        tableFrame.grid_rowconfigure(0, weight=1)
        tableFrame.grid_columnconfigure(0, weight=1)   
        tableFrame.grid_columnconfigure(1, weight=3)

        orderTableFrame.grid_rowconfigure(0, weight=1)
        orderTableFrame.grid_columnconfigure(0, weight=3)   
        orderTableFrame.grid_columnconfigure(1, weight=1)

                # ---- LEFT TABLE + SCROLLBAR ----
        leftScroll = tk.Scrollbar(tableFrame, orient="vertical", command=self.orderTable.yview)
        self.table.configure(yscrollcommand=leftScroll.set)

        #self.orderTable.grid(row=0, column=0, sticky="nsew")
        leftScroll.grid(row=0, column=0, sticky="nse")  # attach scrollbar to right side of left table

        # ---- RIGHT TABLE + SCROLLBAR ----
        rightScroll = tk.Scrollbar(orderTableFrame, orient="vertical", command=self.table.yview)
        self.orderTable.configure(yscrollcommand=rightScroll.set)

        #self.table.grid(row=0, column=1, sticky="nsew")
        rightScroll.grid(row=0, column=1, sticky="nsw")  # scrollbar hugs right side
        # Input Fields
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Qty Prepared:").grid(row=0, column=0, padx=5)
        self.qty_entry = tk.Entry(input_frame)
        self.qty_entry.grid(row=0, column=1, padx=5)
        self.qty_entry.bind("<Return>", self.manuallyValidate)
        self.table.bind("<<TreeviewSelect>>", self.loadCustomerOrders)
        self.orderTable.bind("<<TreeviewSelect>>", self.loadCustomerOrders)

        tk.Label(input_frame, text="Scan Barcode:").grid(row=1, column=0, padx=5)
        self.barcode_entry = tk.Entry(input_frame)
        self.barcode_entry.grid(row=1, column=1, padx=5)
        self.barcode_entry.bind("<Return>", self.manuallyValidate)

        # Status Message
        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Done Button
        tk.Button(self, text="Finish Validation",command=self.validate_barcode).pack(pady=10)
        #self.bind_all("<Key>", self.barcodeScanner)
        self.loadCustomers()
        
    def loadCustomerOrders(self,event):
        selectedCustomer = self.orderTable.selection()
        selectedCustomer = self.orderTable.item(selectedCustomer[0], 'values')[0]
        print("Loading customer orders for:", selectedCustomer)
        if not selectedCustomer:
            return
        DB_FILE = "inventory.db"
        self.table.delete(*self.table.get_children())
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM packingList WHERE customer=?", (selectedCustomer,))
            for row in cursor.fetchall():
                self.table.insert("", "end", values=row)

    def loadCustomers(self):
        self.orderTable.delete(*self.orderTable.get_children())
        DB_FILE = "inventory.db"
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT customer FROM packingList WHERE status='Pending'")
            for row in cursor.fetchall():
                self.orderTable.insert("", "end", values=row)
    def orderSelect(self, event):
        selected_item = self.orderTable.selection()
        if selected_item:
            print("selected item:", selected_item[0])
    def barcodeScanner(self, event):
        """Capture barcode scanner input"""
        self.scanned_code
        if not str(event.widget).startswith(str(self)):
            return
        if event.keysym == "Return":
            if self.scanned_code:
                print("Scanned (in ScanFrame):", self.scanned_code)
                self.scanned_code = ""
        elif len(event.char) == 1:
            self.scanned_code += event.char
    def manuallyValidate(self,event=None):
        self.scanned_code
        self.scanned_code = self.barcode_entry.get().strip()
        self.validate_barcode(self.scanned_code)
    def validate_barcode(self, barcode,event=None):
            """Validate scanned barcode and prepared quantity"""
            self.qty_str = self.qty_entry.get().strip()
            if self.qty_str == "":
                self.qty_str = "1"
            # Quantity must be an integer
            if not self.qty_str.isdigit():
                self.status_label.config(text="❌ Wrong Quantity", fg="red")
                return
            qty = int(self.qty_str)
            print(f"Validating barcode: {barcode} with qty {qty}")
            # Check if barcode exists in list
            with sqlite3.connect("inventory.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ItemCode FROM packingList")
                self.valid_barcodes = {row[0] for row in cursor.fetchall()}
            if barcode not in self.valid_barcodes:
#                self.status_label.config(text="❌ Wrong Item", fg="red")
                self.barcode_entry.delete(0, tk.END)
                messagebox.showerror("Error", f"Item code {barcode} not found in packing list.")
                return
            self.deductItem(barcode, qty)


            self.barcode_entry.delete(0, tk.END)
    def deductItem(self,barcode, qty):
        selectedCustomer = self.orderTable.selection()
        selectedCustomer = self.orderTable.item(selectedCustomer[0], 'values')[0]
        print("Loading customer orders for:", selectedCustomer)
        if not selectedCustomer:
            messagebox.showerror("Error", "Please select a customer first.")
            return 
        with sqlite3 .connect("inventory.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT itemCode, qtyOrdered , status ,qtyPrepared FROM packingList WHERE ItemCode=? AND customer=?", (barcode,selectedCustomer))
                result = cursor.fetchone()
                if result[0] == barcode:
                    if result[2] == "Done":
                        #self.status_label.config(text="✅ Already Done", fg="green")
                        self.barcode_entry.delete(0, tk.END)
                        messagebox.showinfo("Info", "This item is already marked as Done.")
                        return
                    elif result[1] == result[3]:
                        cursor.execute("UPDATE packingList SET status='Done' WHERE ItemCode=? AND Customer=? ", (barcode, selectedCustomer))
                        cursor.execute("UPDATE final_inventory SET qtyPartNumber=qtyPartNumber-? WHERE finalItemcode=?", (result[1], barcode))
                        conn.commit()
                    elif result[1] > result[3]:
                        cursor.execute("UPDATE packingList SET qtyPrepared=qtyPrepared+? WHERE ItemCode=? AND Customer=?", (qty,barcode,selectedCustomer))
    def checkAllDone(self):
        customer = self.orderTable.selection()
        customer = self.orderTable.item(customer[0], 'values')[0]
        print("Loading customer orders for:", customer)
        with sqlite3.connect("inventory.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM packingList WHERE status='Pending' AND customer=?", (customer,))
                pending_count = cursor.fetchone()[0]
                if pending_count == 0:
                    cursor.execute("UPDATE packingList SET status='Done' WHERE customer=?", (customer,))
                    conn.commit()
                    messagebox.showinfo("Info", f"All items for {customer} are marked as Done.")
                    self.table.delete(*self.table.get_children())
                    self.orderTable.delete(*self.orderTable.get_children())
                    self.loadCustomers()
