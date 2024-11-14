from fastapi import FastAPI, HTTPException, Query
from app.models import key_helper
from app.database import key_collection
from app.schemas import KeySchema, UpdateKeyModel
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_allowed_key_types(user_type):
    if user_type == "Guest":
        return ["Guest", "Cleaners", "Maintenance"]
    elif user_type == "Cleaners":
        return ["Cleaners", "Guest"]
    elif user_type == "Maintenance":
        return ["Maintenance"]
    else:
        return []

@app.post("/keys", response_model=KeySchema)
async def create_key(key: KeySchema):
    key = key.dict()
    result = await key_collection.insert_one(key)
    new_key = await key_collection.find_one({"_id": result.inserted_id})
    return key_helper(new_key)

@app.get("/keys", response_model=List[KeySchema])
async def get_keys():
    keys = []
    async for key in key_collection.find():
        keys.append(key_helper(key))
    return keys

@app.put("/keys/{id}", response_model=KeySchema)
async def update_key(id: str, key: UpdateKeyModel):
    key_data = {k: v for k, v in key.dict().items() if v is not None}
    if key_data:
        update_result = await key_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": key_data}
        )
        if update_result.modified_count == 1:
            updated_key = await key_collection.find_one({"_id": ObjectId(id)})
            if updated_key:
                return key_helper(updated_key)
    existing_key = await key_collection.find_one({"_id": ObjectId(id)})
    if existing_key:
        return key_helper(existing_key)
    raise HTTPException(status_code=404, detail=f"Key {id} not found")

@app.delete("/keys/{id}")
async def delete_key(id: str):
    delete_result = await key_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Key deleted"}
    raise HTTPException(status_code=404, detail=f"Key {id} not found")

@app.post("/webhook/keys")
async def handle_webhook(event: dict):
    event_type = event.get("eventType")
    data = event.get("data")
    if not event_type or not data:
        raise HTTPException(status_code=400, detail="Invalid event data")

    if event_type == "create":
        result = await key_collection.insert_one(data)
        return {"message": "Key created", "id": str(result.inserted_id)}
    elif event_type == "update":
        id = data.get("id")
        if not id:
            raise HTTPException(status_code=400, detail="ID is required for update")
        update_result = await key_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if update_result.modified_count == 1:
            return {"message": "Key updated"}
        else:
            raise HTTPException(status_code=404, detail=f"Key {id} not found")
    elif event_type == "delete":
        id = data.get("id")
        if not id:
            raise HTTPException(status_code=400, detail="ID is required for delete")
        delete_result = await key_collection.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            return {"message": "Key deleted"}
        else:
            raise HTTPException(status_code=404, detail=f"Key {id} not found")
    else:
        raise HTTPException(status_code=400, detail="Invalid event type")

@app.post("/keys/assign", response_model=KeySchema)
async def assign_key(user_type: str = Query(..., description="User type requesting a key")):
    allowed_key_types = get_allowed_key_types(user_type)
    key = await key_collection.find_one(
        {"type": {"$in": allowed_key_types}, "status": "Returned"}
    )
    if key:
        await key_collection.update_one(
            {"_id": key["_id"]},
            {"$set": {"status": "In Use", "assigned_to": user_type}}
        )
        updated_key = await key_collection.find_one({"_id": key["_id"]})
        return key_helper(updated_key)
    else:
        raise HTTPException(status_code=404, detail="No available keys for your user type")

@app.post("/keys/return/{key_id}")
async def return_key(key_id: str):
    key = await key_collection.find_one({"key_id": key_id})
    if key:
        await key_collection.update_one(
            {"_id": key["_id"]},
            {"$set": {"status": "Returned", "assigned_to": ""}}
        )
        return {"message": f"Key {key_id} returned successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Key {key_id} not found")

@app.post("/keys/monthly_inspection")
async def monthly_inspection():
    await key_collection.update_many(
        {}, {"$set": {"status": "Under Inspection", "assigned_to": "Inspector"}}
    )
    await key_collection.update_many({}, {"$set": {"status": "Returned", "assigned_to": ""}})
    return {"message": "Monthly inspection completed"}
