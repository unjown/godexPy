import sqlite3
import random
import string

# Connect to database (or create if not exists)
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()


# Helper functions to generate random data
def random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_email(name):
    domains = ["gmail.com", "yahoo.com", "outlook.com"]
    return f"{name.lower()}{random.randint(1,999)}@{random.choice(domains)}"

def random_phone():
    return f"+{random.randint(1,99)}-{random.randint(100000000,999999999)}"

def random_country():
    countries = ["USA", "UK", "China", "Germany", "India", "Brazil", "Canada"]
    return random.choice(countries)

# Insert random suppliers
for _ in range(20):
    supplierCode = random_string()
    supplierName = f"Supplier_{random_string(4)}"
    country = random_country()
    email = random_email(supplierName)
    contactPerson = f"Person_{random_string(3)}"
    contactNumber = random_phone()
    facebookPage = f"fb.com/{supplierName.lower()}"
    webPage = f"www.{supplierName.lower()}.com"
    shippingNotes = "Fast shipping"

    cursor.execute("""
        INSERT OR IGNORE INTO suppliers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (supplierCode, supplierName, country, email, contactPerson, contactNumber, facebookPage, webPage, shippingNotes))

# Insert random raw inventory
for _ in range(20):
    supplierCode = random_string()
    supplierName = f"Supplier_{random_string(4)}"
    partNumber = f"PN-{random.randint(1000,9999)}"
    qtyPerMotherBox = random.randint(10, 100)
    qtyPerInnerBox = random.randint(1, 10)
    itemDescription = f"Item_{random_string(5)}"
    unitOfMeasurement = random.choice(["pcs", "kg", "m", "liters"])
    materialType = random.choice(["Plastic", "Metal", "Wood", "Glass"])
    color = random.choice(["Red", "Blue", "Green", "Black", "White"])
    partCostPerPiece = f"${random.uniform(1, 100):.2f}"
    shelfNumber = str(random.randint(1, 20))
    shelfLocation = f"Aisle-{random.randint(1,10)}"
    warehouseNumber = str(random.randint(1, 5))
    warehouseLocation = f"WH-{random.randint(1,5)}"

    cursor.execute("""
        INSERT OR IGNORE INTO raw_inventory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (supplierCode, supplierName, partNumber, qtyPerMotherBox, qtyPerInnerBox, itemDescription,
          unitOfMeasurement, materialType, color, partCostPerPiece, shelfNumber, shelfLocation,
          warehouseNumber, warehouseLocation))

# Insert random final inventory
for _ in range(20):
    customerCode = random_string()
    customerName = f"Customer_{random_string(4)}"
    partNumber = f"PN-{random.randint(1000,9999)}"
    qtyPartNumber = random.randint(1, 500)
    finalItemcode = f"FI-{random.randint(10000,99999)}"
    itemDescription = f"FinalItem_{random_string(5)}"
    barcodeNumber = f"BC-{random.randint(100000,999999)}"
    shelfNumber = str(random.randint(1, 20))
    shelfLocation = f"Aisle-{random.randint(1,10)}"
    warehouseNumber = str(random.randint(1, 5))
    warehouseLocation = f"WH-{random.randint(1,5)}"

    cursor.execute("""
        INSERT OR IGNORE INTO final_inventory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (customerCode, customerName, partNumber, qtyPartNumber, finalItemcode, itemDescription,
          barcodeNumber, shelfNumber, shelfLocation, warehouseNumber, warehouseLocation))
# Insert random packing list
for _ in range(20):
    itemCode = f"IC-{random.randint(10000,99999)}"
    itemName = f"Item_{random_string(5)}"
    qtyOrdered = random.randint(1, 200)
    shelfNumber = str(random.randint(1, 20))
    warehouseNumber = str(random.randint(1, 5))
    PO = f"PO-{random.randint(1000,9999)}"
    customer = f"Customer_{random_string(4)}"
    date = f"2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    status = random.choice(["Pending", "Processing", "Shipped"])
    qtyPrepared = random.randint(0, qtyOrdered)  # must be ≤ qtyOrdered

    cursor.execute("""
        INSERT INTO packingList 
        (ItemCode, itemName, qtyOrdered, shelfNumber, warehouseNumber, PO, Customer, Date, Status, qtyPrepared)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (itemCode, itemName, qtyOrdered, shelfNumber, warehouseNumber, PO, customer, date, status, qtyPrepared))

# Commit and close
conn.commit()
conn.close()

print("✅ Random data inserted successfully!")
