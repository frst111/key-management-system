def key_helper(key) -> dict:
    return {
        "id": str(key["_id"]),
        "key_id": key["key_id"],
        "type": key["type"],  
        "status": key["status"], 
        "assigned_to": key.get("assigned_to", ""),
    }
