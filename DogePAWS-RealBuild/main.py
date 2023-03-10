# from fastapi import FastAPI
# from typing import List

# from flask import render_template
# from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import RedirectResponse

from Models.product import Product
from Models.order import Order
from Models.payment import Payment
from Models.employee import Employee
from Models.shift import Shift
from Models.store import Store
from Models.inventory import Inventory
from app import app

@app.get("/")
async def read_root(request: Request):
    return RedirectResponse("/landing")

@app.get("/landing")
async def read_landing():
    return {"message": "Welcome to DogePAWS!"}


# Create a new product
@app.post("/products")
async def create_product(product: Product):
    # Code to create a new product
    return {"message": "Product created"}

# Get all products
@app.get("/products")
async def get_all_products():
    # Code to retrieve all products
    return {"message": "Products retrieved"}

# Get a product by ID
@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int):
    # Code to retrieve a product by ID
    return {"message": f"Product with ID {product_id} retrieved"}

# Create a new order
@app.post("/orders")
async def create_order(order: Order):
    # Code to create a new order
    return {"message": "Order created"}

# Get all orders
@app.get("/orders")
async def get_all_orders():
    # Code to retrieve all orders
    return {"message": "Orders retrieved"}

# Get an order by ID
@app.get("/orders/{order_id}")
async def get_order_by_id(order_id: int):
    # Code to retrieve an order by ID
    return {"message": f"Order with ID {order_id} retrieved"}

# Create a new payment
@app.post("/payments")
async def create_payment(payment: Payment):
    # Code to create a new payment
    return {"message": "Payment created"}

# Get all payments
@app.get("/payments")
async def get_all_payments():
    # Code to retrieve all payments
    return {"message": "Payments retrieved"}

# Get a payment by ID
@app.get("/payments/{payment_id}")
async def get_payment_by_id(payment_id: int):
    # Code to retrieve a payment by ID
    return {"message": f"Payment with ID {payment_id} retrieved"}

# Create a new employee
@app.post("/employees")
async def create_employee(employee: Employee):
    # Code to create a new employee
    return {"message": "Employee created"}

# Get all employees
@app.get("/employees")
async def get_all_employees():
    # Code to retrieve all employees
    return {"message": "Employees retrieved"}

# Get an employee by ID
@app.get("/employees/{employee_id}")
async def get_employee_by_id(employee_id: int):
    # Code to retrieve an employee by ID
    return {"message": f"Employee with ID {employee_id} retrieved"}

# Create a new shift
@app.post("/shifts")
async def create_shift(shift: Shift):
    # Code to create a new shift
    return {"message": "Shift created"}

# Get all shifts
@app.get("/shifts")
async def get_all_shifts():
    # Code to retrieve all shifts
    return {"message": "Shifts retrieved"}

# Get a shift by ID
@app.get("/shifts/{shift_id}")
async def get_shift_by_id(shift_id: int):
    # Code to retrieve a shift by ID
    return {"message": f"Shift with ID {shift_id} retrieved"}

# Create a new store
@app.post("/stores")
async def create_store(store: Store):
    # Code to create a new store
    return {"message": "Store created"}

# Get all stores
@app.get("/stores")
async def get_all_stores():
    # Code to retrieve all stores
    return {"message": "Stores retrieved"}

# Get a store by ID
@app.get("/stores/{store_id}")
async def get_store_by_id(store_id: int):
    # Code to retrieve a store by ID
    return {"message": f"Store with ID {store_id} retrieved"}

# Create a new inventory
@app.post("/inventory")
async def create_inventory(inventory: Inventory):
    # Code to create a new inventory
    return {"message": "Inventory created"}

# Get all inventory
@app.get("/inventory")
async def get_all_inventory():
    # Code to retrieve all inventory
    return {"message": "Inventory retrieved"}

# Get inventory for a store by ID
@app.get("/inventory/{store_id}")
async def get_inventory_by_store_id(store_id: int):
    # Code to retrieve inventory for a store by ID
    return {"message": f"Inventory for store with ID {store_id} retrieved"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
