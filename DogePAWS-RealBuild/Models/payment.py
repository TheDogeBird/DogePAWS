from pydantic import BaseModel

class Payment(BaseModel):
    payment_type: str
    payment_amount: float
    payment_date: str
