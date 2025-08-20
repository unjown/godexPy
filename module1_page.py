import tkinter as tk
from tkinter import ttk
import csv
import os
from tkinter import messagebox
import webbrowser
import win32print
import win32ui
class Module1Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
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
    def MainMenu(self):
        self.controller.show_frame("MainMenuPage")

# ====================
# SUBMODULE A - Supplier Management
# ====================
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser


class SupplierManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.CSV_FILE = "suppliers.csv"

        self.CSV_COLUMNS = [
    "Supplier Number", "Supplier Name", "Country", "Email",
    "Contact Person", "Contact Num.", "FB Page", "Web Page", "Shipping Notes"
]
        # Side Panel (Main Menu)
        self.menu_panel = tk.Frame(self, bg="#2c3e50", width=200)
        self.menu_panel.pack(side="left", fill="y")

        tk.Button(self.menu_panel, text="Main Menu", bg="#2c3e50", fg="white", font=("Arial", 14, "bold"),command=lambda: self.controller.MainMenu()).pack(pady=10)
        
        btn_supplier = tk.Button(self.menu_panel, text="Supplier Management", width=20,command=lambda: self.controller.show_subpage("supplier"))
        btn_supplier.pack(pady=5)

        tk.Button(self.menu_panel, text="Raw Inventory", width=20,command=lambda: self.controller.show_subpage("raw")).pack(pady=5)
        tk.Button(self.menu_panel, text="Final Inventory", width=20,command=lambda: self.controller.show_subpage("final")).pack(pady=5)

        # Main Content
        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Hide Menu Button
        #btn_close_menu = tk.Button(content_frame, text="❌ Close Menu", command=self.toggle_menu)
       # btn_close_menu.grid(row=0, column=0, sticky="w", columnspan=2)

        # Form Labels and Entries
        form_frame = tk.Frame(content_frame)
        form_frame.grid(row=1, column=0, sticky="nw")

        tk.Label(form_frame, text="supplierNumber:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=2)
        self.supplierNumber = tk.Entry(form_frame, width=20)
        self.supplierNumber.grid(row=0, column=1, sticky="w", padx=(0, 5))

        tk.Label(form_frame, text="supplierName:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=2)
        self.supplierName = tk.Entry(form_frame, width=20)
        self.supplierName.grid(row=1, column=1, sticky="w", padx=(0, 5))

        tk.Label(form_frame, text="country:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", pady=2)
        self.country = tk.Entry(form_frame, width=20)
        self.country.grid(row=2, column=1, sticky="w", padx=(0, 5))

        tk.Label(form_frame, text="email:", font=("Arial", 10)).grid(row=3, column=0, sticky="e", pady=2)
        self.email = tk.Entry(form_frame, width=20)
        self.email.grid(row=3, column=1, sticky="w", padx=(0, 5))

        tk.Label(form_frame, text="Contact Person:", font=("Arial", 10)).grid(row=4, column=0, sticky="e", pady=2)
        self.contact_name = tk.Entry(form_frame, width=20)
        self.contact_name.grid(row=4, column=1, sticky="w", padx=(0, 5))

        tk.Label(form_frame, text="Contact Number:", font=("Arial", 10)).grid(row=5, column=0, sticky="e", pady=2)
        self.contact_number = tk.Entry(form_frame, width=20)
        self.contact_number.grid(row=5, column=1, sticky="e")

        tk.Label(form_frame, text="Facebook Page:", font=("Arial", 10)).grid(row=6, column=0, sticky="e", pady=2)
        self.Facebook = tk.Entry(form_frame, width=20)
        self.Facebook.grid(row=6, column=1, sticky="e")

        tk.Label(form_frame, text="Web Page:", font=("Arial", 10)).grid(row=7, column=0, sticky="e", pady=2)
        self.Web = tk.Entry(form_frame, width=20)
        self.Web.grid(row=7, column=1, sticky="e")

        tk.Label(form_frame, text="Shipping Notes:", font=("Arial", 10)).grid(row=8, column=0, sticky="e", pady=2)
        self.Shipping = tk.Entry(form_frame, width=20)
        self.Shipping.grid(row=8, column=1, sticky="e")
        # Action Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.grid(row=1, column=1, sticky="ne", padx=10)

        actions = [
            ("Add", self.add_supplier),
            ("Edit", self.edit_supplier),
            ("Delete", self.delete_supplier),
            ("Visit Web...", lambda: self.controller.open_web(self.Web.get()) if hasattr(self.controller, "open_web") else None),
            ("Load Column", self.onSelect)
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
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Make the table area resizable
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        self.load_csv_data()
        #self.tree.bind("<<TreeviewSelect>>", self.onSelect)


#def toggle_menu(self):
    #if self.menu_visible:
    #    self.menu_panel.pack_forget()
     #   self.menu_visible = False
      #  self.btn_toggle_menu.config(text="📂 Open Menu")
    #else:
     #   self.menu_panel.pack(side="left", fill="y")  # Always left
      #  self.menu_visible = True
       # self.btn_toggle_menu.config(text="❌ Close Menu")

# -------------------------------
# CSV functions kdsopfjisfhgjdfjhkjbgjbfgjnbfjdnsjkflajsdfkjsdkjfhsdf I love u GPT.. but ur also useless
# --------------
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
    def loadColumn(self):
        print("LoadColumn")        
    def load_csv_data(self):

        if not os.path.exists(self.CSV_FILE):
            with open(self.CSV_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.CSV_COLUMNS)
            return

        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            self.tree.delete(*self.tree.get_children())  # Clear table
            for row in reader:
                values = [row[col] for col in self.CSV_COLUMNS]
                self.tree.insert("", "end", values=values)

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
            self.Shipping.get()
        ]

        if not data[0]:  # Require Supplier Number
            messagebox.showwarning("Missing Info", "Supplier Number is required.")
            return

        with open(self.CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

        self.tree.insert("", "end", values=data)
        self.clear_form()

    def delete_supplier(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a supplier to delete.")
            return

        values_to_delete = self.tree.item(selected[0])["values"]
        self.tree.delete(selected[0])

        rows = []
        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                if row != values_to_delete:
                    rows.append(row)

        with open(self.CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

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

        if not new_data[0]:
            messagebox.showwarning("Missing Info", "Supplier Number is required.")
            return

        selected_item = selected[0]
        old_data = self.tree.item(selected_item)["values"]

        self.tree.item(selected_item, values=new_data)

        # Update the CSV
        updated_rows = []
        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                if row == old_data:
                    updated_rows.append(new_data)
                else:
                    updated_rows.append(row)

        with open(self.CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(updated_rows)

        self.clear_form()

    def fill_form_from_tree(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])['values']
        entries = [
            self.supplierNumber, self.supplierName, self.country, self.email,
            self.contact_name, self.contact_number, self.Facebook, self.Web, self.Shipping
        ]
        for entry, value in zip(entries, values):
            entry.delete(0, tk.END)
            entry.insert(0, value)

    def clear_form(self):
        for widget in [self.supplierNumber, self.supplierName, self.country, self.email,
                    self.contact_name, self.contact_number, self.Facebook, self.Web, self.Shipping]:
            widget.delete(0, tk.END)
    

# ====================
# SUBMODULE B - Raw Inventory Entry
# ====================
class RawInventoryEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Side Panel (Main Menu)
        self.CSV_FILE = "raw_inventory.csv"

        self.CSV_COLUMNS = [
    "Customer Code", "Customer Name", "Part Number", "Qty Per Mother Box",
    "Qty Per Inner Box", "Item Description", "Facebook", "Unit Of Measurement",
    "Material Type", "Color", "Part Cost Per Piece", "Shelf Number",
    "Shelf Location", "Warehouse Number", "Warehouse Location"
]
        
        self.menu_panel = tk.Frame(self, bg="#2c3e50", width=200)
        self.menu_panel.pack(side="left", fill="y")

        tk.Button(self.menu_panel, text="Main Menu", bg="#2c3e50", fg="white", font=("Arial", 14, "bold"),command=lambda: self.controller.MainMenu()).pack(pady=10)

        btn_supplier = tk.Button(self.menu_panel, text="Supplier Management", width=20,command=lambda: self.controller.show_subpage("supplier"))
        btn_supplier.pack(pady=5)

        tk.Button(self.menu_panel, text="Raw Inventory", width=20,command=lambda: self.controller.show_subpage("raw")).pack(pady=5)
        tk.Button(self.menu_panel, text="Final Inventory", width=20,command=lambda: self.controller.show_subpage("final")).pack(pady=5)

        #Main content --------
        content_frame = tk.Frame(self)
        content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        tk.Label(content_frame, text="Raw Inventory", font=("Arial", 14, "bold")).grid(pady=10)


        form_frame = tk.Frame(content_frame)
        form_frame.grid(row=2, column=0, sticky="nw")
        searchFrame = tk.Frame(content_frame)
        searchFrame.grid(row=1, column=0, sticky="nw")
        tk.Label(searchFrame, text="Search Raw Part (Part Number / Shelf / Warehouse):").grid(row=1,column=0,sticky="w")
        self.search_entry = tk.Entry(searchFrame, width=50)
        self.search_entry.grid(row=1,column=1,sticky="w")
        tk.Button(searchFrame, text="Search", command=self.search).grid(row=1, column=2, sticky="w")
        fields = [
    ("Customer Code", "customerCode"),
    ("Customer Name", "customerName"),
    ("Part Number", "partNumber"),
    ("Qty per Mother Box", "qtyPerMotherBox"),
    ("Qty per Innerbox ", "qtyPerInnerBox"),
    ("Item Description", "itemDescription"),
    ("Facebook", "Facebook"),   
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
            tk.Label(form_frame, text=label_text + ":", font=("Arial", 10)).grid(row=idx +1 , column=0, sticky="e", pady=2)
            setattr(self, var_name, tk.Entry(form_frame, width=30))
            getattr(self, var_name).grid(row=idx +1, column=1, sticky="w", padx=(0, 5))
        for idx, (label_text, var_name) in enumerate(secondField):
            tk.Label(form_frame, text=label_text + ":", font=("Arial", 10)).grid(row=idx+1 , column=2, sticky="e", pady=2)
            setattr(self, var_name, tk.Entry(form_frame, width=30))
            getattr(self, var_name).grid(row=idx+1, column=3, sticky="w", padx=(0, 5))
        table_frame = tk.Frame(content_frame)
        table_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)

        columns = ( "Code",
    "Customer Names",
    "Part Number",
    "Qty Per Mother Box",
    "Qty Per Innerbox Of The Mother Box",
    "Item Description",
    "Facebook",
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

        self.check_var = tk.IntVar() # Variable to store the checkbox state
        self.checkbox = tk.Checkbutton(form_frame, text="Print Label", variable=self.check_var)
        self.checkbox.grid(pady=5,row=4,column=4)
        #tk.Label(form_frame, text="New Raw Inventory Entry").grid(pady=5,row=2,column=4)
        tk.Button(form_frame, text="Load Selected Column", command=self.onSelect).grid(pady=5,row=2,column=4)
        tk.Button(form_frame, text="Save to raw_inventory", command=self.add_supplier).grid(pady=5,row=3,column=4)
        self.load_csv_data()

#============
#RAHHHHHHHHH MORE CSV LOADING IM SURE U CAN JUST CALL ALL DIS IN A FUNCTION IN MODULE(aka im reminding myself to test this in the future)
#==========
    def search(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Search", "Enter text to search.")
            return

        self.tree.selection_remove(self.tree.selection())  # clear previous selection
        found = False
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, "values")
            # Check each column for partial match
            if any(query in str(v).lower() for v in values):
                self.tree.selection_add(item_id)
                self.tree.see(item_id)  # scroll into view
                found = True

        if not found:
            messagebox.showinfo("Search", "No matching records found.")

    def onSelect(self):
        print("dsjofhidsuhfuidh")
        selected_item = self.tree.selection()
        if not selected_item:
            return
        row_values = self.tree.item(selected_item)["values"]
        self.customerCode.delete(0, tk.END)
        self.customerCode.insert(0, row_values[0])

        self.customerName.delete(0, tk.END)
        self.customerName.insert(0, row_values[1])

        self.partNumber.delete(0, tk.END)
        self.partNumber.insert(0, row_values[2])

        self.qtyPerMotherBox.delete(0, tk.END)
        self.qtyPerMotherBox.insert(0, row_values[3])

        self.qtyPerInnerBox.delete(0, tk.END)
        self.qtyPerInnerBox.insert(0, row_values[4])

        self.itemDescription.delete(0, tk.END)
        self.itemDescription.insert(0, row_values[5])

        self.Facebook.delete(0, tk.END)
        self.Facebook.insert(0, row_values[6])

        self.unitOfMeasurement.delete(0, tk.END)
        self.unitOfMeasurement.insert(0, row_values[7])

        self.materialType.delete(0, tk.END)
        self.materialType.insert(0, row_values[8])
        
        self.color.delete(0, tk.END)
        self.color.insert(0, row_values[9])
        
        self.partCostPerPiece.delete(0, tk.END)
        self.partCostPerPiece.insert(0, row_values[10])
        
        self.shelfNumber.delete(0, tk.END)
        self.shelfNumber.insert(0, row_values[11])
        
        self.shelfLocation.delete(0, tk.END)
        self.shelfLocation.insert(0, row_values[12])

        self.warehouseNumber.delete(0, tk.END)
        self.warehouseNumber.insert(0, row_values[13])

        self.warehouseLocation.delete(0, tk.END)
        self.warehouseLocation.insert(0, row_values[14])
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
      
    def load_csv_data(self):

        if not os.path.exists(self.CSV_FILE):
            with open(self.CSV_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.CSV_COLUMNS)
            return

        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            self.tree.delete(*self.tree.get_children())  # Clear table
            for row in reader:
                values = [row[col] for col in self.CSV_COLUMNS]
                self.tree.insert("", "end", values=values)

    def add_supplier(self):
        print(self.check_var.get())
        data = [
self.customerCode.get(),
self.customerName.get(),
self.partNumber.get(),
self.qtyPerMotherBox.get(),
self.qtyPerInnerBox.get(),
self.itemDescription.get(),
self.Facebook.get(),
self.unitOfMeasurement.get(),
self.materialType.get(),
self.color.get(),
self.partCostPerPiece.get(),
self.shelfNumber.get(),
self.shelfLocation.get(),
self.warehouseNumber.get(),
self.warehouseLocation.get()

        ]

        if not data[0]:  # Require Supplier Number
            messagebox.showwarning("Missing Info", "Supplier Number is required.")
            return

        with open(self.CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

        self.tree.insert("", "end", values=data)
        self.clear_form()
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

        
    def delete_supplier(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a supplier to delete.")
            return

        values_to_delete = self.tree.item(selected[0])["values"]
        self.tree.delete(selected[0])

        rows = []
        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                if row != values_to_delete:
                    rows.append(row)

        with open(self.CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def edit_supplier(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a supplier to edit.")
            return

        new_data = [
self.customerCode.get(),
self.customerName.get(),
self.partNumber.get(),
self.qtyPerMotherBox.get(),
self.qtyPerInnerBox.get(),
self.itemDescription.get(),
self.Facebook.get(),
self.unitOfMeasurement.get(),
self.materialType.get(),
self.color.get(),
self.partCostPerPiece.get(),
self.shelfNumber.get(),
self.shelfLocation.get(),
self.warehouseNumber.get(),
self.warehouseLocation.get()

        ]

        if not new_data[0]:
            messagebox.showwarning("Missing Info", "Supplier Number is required.")
            return

        selected_item = selected[0]
        old_data = self.tree.item(selected_item)["values"]

        self.tree.item(selected_item, values=new_data)

        # Update the CSV
        updated_rows = []
        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                if row == old_data:
                    updated_rows.append(new_data)
                else:
                    updated_rows.append(row)

        with open(self.CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(updated_rows)

        self.clear_form()

    def fill_form_from_tree(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])['values']
        entries = [
            self.customerCode, self.customerName, self.partNumber, self.qtyPerMotherBox,
            self.qtyPerInnerBox, self.itemDescription, self.Facebook, self.unitOfMeasurement,
            self.materialType, self.color, self.partCostPerPiece, self.shelfNumber,
            self.shelfLocation, self.warehouseNumber, self.warehouseLocation
]
        for entry, value in zip(entries, values):
            entry.delete(0, tk.END)
            entry.insert(0, value)

    def clear_form(self):
        for widget in [
            self.customerCode, self.customerName, self.partNumber, self.qtyPerMotherBox,
            self.qtyPerInnerBox, self.itemDescription, self.Facebook, self.unitOfMeasurement,
            self.materialType, self.color, self.partCostPerPiece, self.shelfNumber,
            self.shelfLocation, self.warehouseNumber, self.warehouseLocation
        ]:
            widget.delete(0, tk.END)

# ====================
# SUBMODULE C - Final Inventory Entry
# ====================
class FinalInventoryEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.CSV_FILE = "final_inventory.csv"

        self.CSV_COLUMNS = [
    "Customer Code",
    "Customer Name",
    "Part Numbers Used",
    "Qty of Said Part Number",
    "Final Itemcode",
    "Item Description",
    "Barcode Number",
    "Shelf Number",
    "Shelf Location",
    "Warehouse Number",
    "Warehouse Location"
]

        # Side Panel (Main Menu)
        self.menu_panel = tk.Frame(self, bg="#2c3e50", width=200)
        self.menu_panel.pack(side="left", fill="y")

        tk.Button(self.menu_panel, text="Main Menu", bg="#2c3e50", fg="white", font=("Arial", 14, "bold"),command=lambda: self.controller.MainMenu()).pack(pady=10)

        btn_supplier = tk.Button(self.menu_panel, text="Supplier Management", width=20,command=lambda: self.controller.show_subpage("supplier"))
        btn_supplier.pack(pady=5)

        tk.Button(self.menu_panel, text="Raw Inventory", width=20,command=lambda: self.controller.show_subpage("raw")).pack(pady=5)
        tk.Button(self.menu_panel, text="Final Inventory", width=20,command=lambda: self.controller.show_subpage("final")).pack(pady=5)

       # tk.Label(self, text="📦 Final Inventory Entry", font=("Arial", 14, "bold")).pack(pady=10)


        content_frame = tk.Frame(self)
        content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        #tk.Label(content_frame, text="📥 Raw Inventory Entry", font=("Arial", 14, "bold")).grid(pady=10)

        # tk.Label(content_frame, text="Search Raw Part (Part Number / Shelf / Warehouse):").grid(row=1,column=0,sticky="w")
        #tk.Entry(content_frame, width=50).grid(row=1,column=1,sticky="w")
        form_frame = tk.Frame(content_frame)
        form_frame.grid(row=2, column=0, sticky="nw")
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
        table_frame = tk.Frame(content_frame)
        table_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)

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

        check_var = tk.IntVar() # Variable to store the checkbox state
        # checkbox = tk.Checkbutton(form_frame, text="Print Label", variable=check_var)
        # checkbox.grid(pady=5,row=4,column=4)
        #tk.Label(form_frame, text="New Raw Inventory Entry").grid(pady=5,row=2,column=4)
        
        self.load_csv_data()


        buttonFrame = tk.Frame(content_frame)
        buttonFrame.grid(row=2, column=1, sticky="ne")
        tk.Button(buttonFrame, text="Save to FInal Inventory").grid(pady=5,row=5,column=4)

        tk.Label(buttonFrame, text="Search Final Item").grid(column=4,row=1)
        tk.Entry(buttonFrame, width=20).grid(pady=5,column=4,row=2)

        tk.Button(buttonFrame, text="Check / Generate Barcode").grid(pady=5,column=4, row=3)
        #tk.Label(buttonFrame, text="Label Preview:").grid(pady=5,column=4, row=6)

        #preview_frame = tk.LabelFrame(buttonFrame, text="30x25mm Label Preview", padx=10, pady=10)
        #preview_frame.grid(pady=10 ,column=4, row=7)
        #tk.Label(preview_frame, text="(Label preview would go here)").grid()

        tk.Button(buttonFrame, text="Print to GoDEX Printer", command=self.print_selected_label_godex).grid(pady=5,column=4,row=4)
     #   tk.Button(form_frame, text="Save to final_inventory").pack()
# ==================
# ;-; more CSV loading 
#==========================
    def onSelect(self):
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

    def loadColumn(self):
        print("LoadColumn")        

    def load_csv_data(self):
        if not os.path.exists(self.CSV_FILE):
            with open(self.CSV_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.CSV_COLUMNS)
            return

        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            self.tree.delete(*self.tree.get_children())  # Clear table
            for row in reader:
                values = [row[col] for col in self.CSV_COLUMNS]
                self.tree.insert("", "end", values=values)

    def add_supplier(self):
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

        if not data[0]:  # Require Customer Code
            messagebox.showwarning("Missing Info", "Customer Code is required.")
            return

        with open(self.CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

        self.tree.insert("", "end", values=data)
        self.clear_form()

    def delete_supplier(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a customer to delete.")
            return

        values_to_delete = self.tree.item(selected[0])["values"]
        self.tree.delete(selected[0])

        rows = []
        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                if row != values_to_delete:
                    rows.append(row)

        with open(self.CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def edit_supplier(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a customer to edit.")
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

        if not new_data[0]:
            messagebox.showwarning("Missing Info", "Customer Code is required.")
            return

        selected_item = selected[0]
        old_data = self.tree.item(selected_item)["values"]

        self.tree.item(selected_item, values=new_data)

        # Update the CSV
        updated_rows = []
        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                if row == old_data:
                    updated_rows.append(new_data)
                else:
                    updated_rows.append(row)

        with open(self.CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(updated_rows)

        self.clear_form()

    def fill_form_from_tree(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])['values']
        entries = [
            self.customerCode, self.customerName, self.partNumbersUsed,
            self.qtyOfSaidPartNumber, self.finalItemcode, self.itemDescription,
            self.barcodeNumber, self.shelfNumber, self.shelfLocation,
            self.warehouseNumber, self.warehouseLocation
        ]
        for entry, value in zip(entries, values):
            entry.delete(0, tk.END)
            entry.insert(0, value)

    def clear_form(self):
        for widget in [
            self.customerCode, self.customerName, self.partNumbersUsed,
            self.qtyOfSaidPartNumber, self.finalItemcode, self.itemDescription,
            self.barcodeNumber, self.shelfNumber, self.shelfLocation,
            self.warehouseNumber, self.warehouseLocation
        ]:
            widget.delete(0, tk.END)
            

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
