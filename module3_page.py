import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

class Module3Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.PackingListCSV = "for_assembly.csv"  # From Module 2
        self.FACSV_COLUMNS = [
            "ItemName", "ItemCode", "QtyOrdered",
            "ShelfNumber", "WarehouseNumber", "PO",
            "Customer", "Date"
        ]

        tk.Label(self, text="🛠️ Module 3: Product Assembly Validation",
                 font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self, text="Main Menu", bg="#2c3e50", fg="white",
                  font=("Arial", 14, "bold"),
                  command=lambda: self.controller.show_frame("MainMenuPage")
                  ).pack(pady=10, anchor='nw')

        # Table of items to validate
        self.table = ttk.Treeview(
            self,   
            columns=("ItemName", "ItemCode", "QtyOrdered", "ShelfNumber", "WarehouseNumber" ,"PO","Customer","Date","Status"),
            show="headings"
        )

        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=80)

        self.table.pack(pady=10, fill="both", expand=True)

        # Input Fields
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Qty Prepared:").grid(row=0, column=0, padx=5)
        self.qty_entry = tk.Entry(input_frame)
        self.qty_entry.grid(row=0, column=1, padx=5)
        self.qty_entry.bind("<Return>", self.validate_barcode)

        tk.Label(input_frame, text="Scan Barcode:").grid(row=1, column=0, padx=5)
        self.barcode_entry = tk.Entry(input_frame)
        self.barcode_entry.grid(row=1, column=1, padx=5)
        self.barcode_entry.bind("<Return>", self.validate_barcode)

        # Status Message
        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Done Button
        tk.Button(self, text="Finish Validation",command=self.validate_barcode).pack(pady=10)

        # Load CSV data
        self.load_csv_data()

    def load_csv_data(self):
        """Load packing list from CSV into the table"""
        self.table.delete(*self.table.get_children())
        self.valid_barcodes = set()

        if not os.path.exists(self.PackingListCSV):
            messagebox.showwarning("Missing File", f"{self.PackingListCSV} not found!")
            return

        with open(self.PackingListCSV, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.table.insert("", "end", values=(
                    row["ItemName"],
                    row["ItemCode"],
                    row["QtyOrdered"],
                    row["ShelfNumber"],
                    row["WarehouseNumber"],
                    row["PO"],
                    row["Customer"],
                    row["Date"],
                    "Pending"
                ))
                # Ensure the barcode column exists before adding
                if row["ItemCode"]:
                    self.valid_barcodes.add(row["ItemCode"])


    def validate_barcode(self, event):
            """Validate scanned barcode and prepared quantity"""
            barcode = self.barcode_entry.get().strip()
            qty_str = self.qty_entry.get().strip()

            # Quantity must be an integer
            if not qty_str.isdigit():
                self.status_label.config(text="❌ Wrong Quantity", fg="red")
                return
            qty = int(qty_str)

            # Check if barcode exists in list
            if barcode not in self.valid_barcodes:
                self.status_label.config(text="❌ Wrong Item", fg="red")
                self.barcode_entry.delete(0, tk.END)
                return
            validated = False
            # Find row in table that matches barcode
            for item_id in self.table.get_children():
                values = list(self.table.item(item_id, "values"))
                item_code = values[1]  # ItemCode column
                ordered_qty = int(values[2])  # QtyOrdered column
                status = values[-1]  # Status column

                if item_code == barcode:
                    if qty == ordered_qty and status != "✔ Done":
                        values[-1] = "✔ Done"
                        self.table.item(item_id, values=values)
                        self.status_label.config(text="✅ Valid item", fg="green")
                        validated = True

                    elif qty != ordered_qty:
                        self.status_label.config(text="❌ Wrong Quantity", fg="red")
                    elif status == "✔ Done":
                        self.status_label.config(text="⚠ Already validated", fg="orange")
                    break

            self.barcode_entry.delete(0, tk.END)
            if validated:
                all_done = all(self.table.item(item_id, "values")[-1] == "✔ Done"
                       for item_id in self.table.get_children())
                if all_done:
                    messagebox.showinfo("Success", "🎉 All items validated!")
                    self.deduct_all_items_from_inventory()
            messagebox.showinfo("Success", "All items validated and inventory updated!")

    def deduct_all_items_from_inventory(self):
        """Deduct all validated items from final_inventory.csv once at the end"""
        inventory_file = "final_inventory.csv"

        if not os.path.exists(inventory_file):
            messagebox.showerror("Error", f"{inventory_file} not found!")
            return

        # Load inventory
        with open(inventory_file, "r", newline="") as file:
            inventory_data = list(csv.DictReader(file))

        # Deduct quantities ONLY for validated items
        for item_id in self.table.get_children():
            values = self.table.item(item_id, "values")
            barcode = values[1].strip()  # ItemCode
            qty_to_deduct = int(values[2])  # QtyOrdered
            status = values[-1]

            if status == "✔ Done":
                found = False
                for row in inventory_data:
                    if row["Final Itemcode"].strip() == barcode:
                        current_qty = int(row["Qty of Said Part Number"])
                        row["Qty of Said Part Number"] = str(max(0, current_qty - qty_to_deduct))
                        found = True
                        break
                if not found:
                    print(f"Barcode {barcode} not found in inventory.")

        # Save updated inventory
        with open(inventory_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=inventory_data[0].keys())
            writer.writeheader()
            writer.writerows(inventory_data)

        # Optionally clear packing list after deduction
        with open(self.PackingListCSV, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.FACSV_COLUMNS)
            writer.writeheader()

        # Refresh table from CSV
        self.load_csv_data()
