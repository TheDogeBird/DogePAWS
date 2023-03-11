# Models/employee.py
from pydantic import BaseModel

class Employee(BaseModel):
    name: str
    role: str
    contact_info: str
