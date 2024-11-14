from pydantic import BaseModel
from typing import Optional

class KeySchema(BaseModel):
    key_id: str
    type: str
    status: str
    assigned_to: Optional[str] = None

class UpdateKeyModel(BaseModel):
    status: Optional[str]
    assigned_to: Optional[str]

    class Config:
        arbitrary_types_allowed = True
