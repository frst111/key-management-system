import asyncio
from database import key_collection

keys_data = [
    {"key_id": "G1", "type": "Guest", "status": "Returned", "assigned_to": ""},
    {"key_id": "G2", "type": "Guest", "status": "Returned", "assigned_to": ""},
    {"key_id": "C1", "type": "Cleaners", "status": "Returned", "assigned_to": ""},
    {"key_id": "C2", "type": "Cleaners", "status": "Returned", "assigned_to": ""},
    {"key_id": "M1", "type": "Maintenance", "status": "Returned", "assigned_to": ""},
    {"key_id": "M2", "type": "Maintenance", "status": "Returned", "assigned_to": ""},
]

async def populate_db():
    await key_collection.delete_many({})
    await key_collection.insert_many(keys_data)
    print("Database populated")

if __name__ == "__main__":
    asyncio.run(populate_db())
