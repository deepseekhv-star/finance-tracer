from pymongo import MongoClient # Import the MongoClient class from the pymongo library
import random

#MONGO_URI = "mongodb+srv://datnguyenhv_db_user:l4bYWMnfga0wzfcj@cluster0.mzdpikg.mongodb.net/?appName=Cluster0"
MONGO_URI = "mongodb+srv://datnguyenhv_db_user:USUM5z3iSiNIGkTd@cluster0.fkuguq0.mongodb.net/?appName=Cluster0"
#MONGO_URI="mongodb+srv://Zyro:zyro9579@cluster0.i423szf.mongodb.net/?appName=Cluster0"
print("MongoDB URI:", MONGO_URI)

client = MongoClient(MONGO_URI)
db = client['finance_tracker']  # Access the 'finance_tracker' database
transactions = db['transactions']  # Access the 'transactions' collection

print("Successfully connected to the database and collection.\n")

db.command("ping")
print("Pinged your deployment. You successfully connected to MongoDB!")
print("Database_name", db.name)
print("Collection_name", transactions.name)

# insert one
'''
my_transaction = {
    "type": "expense",
    "amount": 50,
    "category": "groceries",
    "description": "Weekly grocery shopping",
    "unit": "USD"
}
transactions.insert_one(my_transaction)
print("Inserted one transaction:", my_transaction)
print("Inserted successfully.\n")
'''

multiple_transactions = []
TYPE = ["in", "out"]
UNIT = ["USD", "EUR", "GBP", "JPY", "AUD"]
CATEGORY_INCOME = ["salary", "freelance", "investment", "gift", "other"]

'''
for i in range(10):
    fake_transaction = {
        "type": random.choice(TYPE),
        "amount": random.randint(10, 1000),
        "category": random.choice(CATEGORY_INCOME) if TYPE[0] == "in" else random.choice(["groceries", "rent", "utilities", "entertainment", "other"]),
        "description": f"Transaction {i+1}",
        "unit": random.choice(UNIT)
    }
    multiple_transactions.append(fake_transaction)
    print(f"Inserted transaction {i+1}: {fake_transaction}")

result = transactions.insert_many(multiple_transactions)
print("\nInserted multiple transactions successfully.")
print("Inserted IDs:", len(result.inserted_ids))
print("Generated IDs:", result.inserted_ids)
'''
'''
my_embedded_transaction = {
    "type": "expense",
    "amount": 150,
    "category": "utilities",
    "description": "Monthly electricity bill",
    "unit": "USD",
    "details": [{
        "due_date": "2024-07-15",
        "paid": False,
        "payment_method": "credit card"
        }]
    }
transactions.insert_one(my_embedded_transaction)
print("\nInserted embedded transaction:", my_embedded_transaction)
'''

print("="*60)
print("Read data")
print("="*60)
all_transactions = transactions.find() # Retrieve all documents from the 'transactions' collection
all_transactions = list(all_transactions)
print(f"Retrieved {len(all_transactions)} documents:")
for trans in all_transactions[:5]:
    print(trans.get("_id", "None"), end=" | ")
    print(trans.get("_type", "Other type"), end=" | ")
    print(trans.get("amount", "No amount"), end="\n")

all_trans_in = transactions.find({"type": "in"})
all_trans_in = list(all_trans_in)
print(f"Retrieved {len(all_trans_in)} income documents:")
for trans_in in all_trans_in:
    print(trans_in)

# get docs with amount greater than 50, less than 100
high_value_transactions = transactions.find({"amount": {"$gt": 50, "$lt": 100}, "UNIT": "USD"})
