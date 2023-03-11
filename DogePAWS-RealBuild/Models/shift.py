# Models/shift.py
from pydantic import BaseModel
from typing import List

from .employee import Employee

class Shift(BaseModel):
    employee: Employee
    shift_start_time: str
    shift_end_time: str
