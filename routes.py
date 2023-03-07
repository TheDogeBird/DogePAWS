from flask import Blueprint, jsonify, request, render_template
from models import User, Product, Category, Supplier, Order, OrderItem, Inventory
import jwt
from datetime import datetime, timedelta
from __main__ import app, db
app_bp = Blueprint('app_bp', __name__)

@app_bp.route('/')
def index():
    return render_template('index.html')

@app_bp.route('/register', methods=['POST'])
def register():
    # implementation for registering a user
    pass

@app_bp.route('/login', methods=['POST'])
def login():
    # implementation for logging in a user
    pass

@app_bp.route('/products', methods=['GET'])
def products():
    # implementation for getting all products
    pass

@app_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # implementation for getting a specific product by id
    pass

@app_bp.route('/categories', methods=['GET'])
def categories():
    # implementation for getting all categories
    pass

@app_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    # implementation for getting a specific category by id
    pass

@app_bp.route('/suppliers', methods=['GET'])
def suppliers():
    # implementation for getting all suppliers
    pass

@app_bp.route('/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    # implementation for getting a specific supplier by id
    pass

@app_bp.route('/orders', methods=['GET'])
def orders():
    # implementation for getting all orders
    pass

@app_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # implementation for getting a specific order by id
    pass

@app_bp.route('/orders', methods=['POST'])
def create_order():
    # implementation for creating an order
    pass

@app_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    # implementation for updating an order by id
    pass

@app_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # implementation for deleting an order by id
    pass

@app_bp.route('/inventory', methods=['GET'])
def inventory():
    # implementation for getting all products with inventory data
    pass

@app_bp.route('/inventory/<int:product_id>', methods=['GET'])
def get_inventory(product_id):
    # implementation for getting inventory data for a specific product by id
    pass

@app_bp.route('/inventory', methods=['POST'])
def add_inventory():
    # implementation for adding inventory data for a specific product
    pass

@app_bp.route('/inventory/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    # implementation for updating inventory data for a specific product by id
    pass

@app_bp.route('/inventory/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    # implementation for deleting inventory data for a specific product by id
    return render_template('register.html')

## TODO::LOGIN --------------------------------------------------