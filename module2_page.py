import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import csv
import os

class Module2Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.CSV_FILE = "final_inventory.csv"
        self.PackingListCSV = "for_assembly.csv"

        # These are the actual columns in final_inventory.csv
        self.CSV_COLUMNS = [
            "ItemName", "ItemCode", "Qty", "ShelfNumber", "WarehouseNumber"
        ]

        # Columns for the packing list
        self.FACSV_COLUMNS = [
            "ItemName", "ItemCode", "QtyOrdered", "ShelfNumber", "WarehouseNumber","PO","Customer","Date"
        ]

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
        columns = ["ItemName", "ItemCode"]
        self.tree = ttk.Treeview(selector_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)

        tk.Button(selector_frame, text="Add →", command=self.addData).pack(pady=5)

        # Preview table
        self.preview_table = ttk.Treeview(preview_frame,
                                          columns=("ItemName", "ItemCode", "QtyOrdered", "ShelfNumber", "WarehouseNumber","PO","Customer","Date"),
                                          show="headings")
        self.preview_table.heading("ItemName", text="Item")
        self.preview_table.heading("ItemCode", text="Code")
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

        # Footer Buttons
        footer = tk.Frame(self)
        footer.pack(pady=10)
        tk.Button(footer, text="Print Packing List", command=self.print_packing_list_ezpl).pack(side="left", padx=10)
        tk.Button(footer, text="Save to for_assembly").pack(side="left", padx=10)

        self.load_csv_data()

    def load_csv_data(self):
        """Load only ItemName and ItemCode into the selector."""
        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            self.tree.delete(*self.tree.get_children())  # Clear table
            for row in reader:
                self.tree.insert("", "end", values=(row["Final Itemcode"], row["Qty of Said Part Number"]))
        if not os.path.exists(self.PackingListCSV):
            with open(self.PackingListCSV, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.FACSV_COLUMNS)

        with open(self.PackingListCSV, 'r', newline='') as f:
            reader = csv.DictReader(f)
            self.preview_table.delete(*self.preview_table.get_children())  # Clear table
            for row in reader:
                values = [row[col] for col in self.FACSV_COLUMNS]
                self.preview_table.insert("", "end", values=values)

    def addData(self):
        

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item first.")
            return

        item_name, item_code = self.tree.item(selected[0], "values")
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

        # Search final_inventory.csv for full item details
        with open(self.CSV_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            full_row = None
            for row in reader:
                if row["Final Itemcode"] == item_name and row["Qty of Said Part Number"] == item_code:
                    full_row = row
                    break

        if full_row:
            # Write to packing list CSV
            with open(self.PackingListCSV, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    full_row["Item Description"],      # ItemName
                    full_row["Final Itemcode"],         # ItemCode
                    qty,                                # QtyOrdered
                    full_row["Shelf Number"],           # ShelfNumber
                    full_row["Warehouse Location"],     # WarehouseNumber
                    POEntry,                            # PO
                    CustomerEntry,                      # Customer
                    DateEntry                           # Date
                ])

            # Update preview table with all columns
            self.preview_table.insert("", "end", values=(
                full_row["Item Description"],
                full_row["Final Itemcode"],
                qty,
                full_row["Shelf Number"],
                full_row["Warehouse Location"],
                POEntry,
                CustomerEntry,
                DateEntry
            ))

            messagebox.showinfo("Success", f"Added {qty} of {item_name}")
        else:
            messagebox.showerror("Error", "Item details not found in inventory.")

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
