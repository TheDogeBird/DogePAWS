from pydantic import BaseModel

class Store(BaseModel):
    name: str
    address: str
    contact_info: str
