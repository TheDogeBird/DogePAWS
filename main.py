from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
import requests
import jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dogepaws!:dogepaws!@localhost/DogePOS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define the database models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'stock': self.stock,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    brand = db.Column(db.String(50))
    size = db.Column(db.String(10))
    color = db.Column(db.String(20))
    room_type = db.Column(db.String(20))
    amenities = db.Column(db.String(500))
    rate = db.Column(db.Float)
    availability = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    custom_properties = db.Column(db.JSON)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'category_id': self.category_id,
            'brand': self.brand,
            'size': self.size,
            'color': self.color,
            'room_type': self.room_type,
            'amenities': self.amenities,
            'rate': self.rate,
            'availability': self.availability,
            'supplier_id': self.supplier_id,
            'custom_properties': self.custom_properties
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    roles = db.relationship('Role', secondary='user_role')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'roles': [r.name for r in self.roles]
        }


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                     )


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(500))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    products = db.relationship('Product', backref='supplier')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    order_items = db.relationship('OrderItem', backref='order')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }


# Define the routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')

        # Check if email is already in use
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'error': 'Email is already in use'}), 409

        # Create a new user
        new_user = User(email=email, password_hash=password, first_name=first_name, last_name=last_name, phone=phone)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_dict()), 201

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401

        # Check password
        if not user.password_hash == password:
            return jsonify({'error': 'Invalid email or password'}), 401

        # Create a JWT token
        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'access_token': token.decode('UTF-8')})

    return render_template('login.html')


@app.route('/products', methods=['GET'])
def products():
    # Get all products
    products = Product.query.all()

    # Convert to dictionary format
    result = [product.to_dict() for product in products]

    return jsonify(result)


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # Get product by ID
    product = Product.query.get(product_id)

    # Check if product exists
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Convert to dictionary format
    result = product.to_dict()

    return jsonify(result)


@app.route('/categories', methods=['GET'])
def categories():
    # Get all categories
    categories = Category.query.all()

    # Convert to dictionary format
    result = [category.to_dict() for category in categories]

    return jsonify(result)


@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    # Get category by ID
    category = Category.query.get(category_id)

    # Check if category exists
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    # Convert to dictionary format
    result = category.to_dict()

    return jsonify(result)


@app.route('/suppliers', methods=['GET'])
def suppliers():
    # Get all suppliers
    suppliers = Supplier.query.all()

    # Convert to dictionary format
    result = [supplier.to_dict() for supplier in suppliers]

    return jsonify(result)


@app.route('/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    # Get supplier by ID
    supplier = Supplier.query.get(supplier_id)

    # Check if supplier exists
    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404

    # Convert to dictionary format
    result = supplier.to_dict()

    return jsonify(result)


@app.route('/orders', methods=['GET'])
def orders():
    # Get all orders
    orders = Order.query.all()

    # Convert to dictionary format
    result = [order.to_dict() for order in orders]

    return jsonify(result)


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # Get order by ID
    order = Order.query.get(order_id)

    # Check if order exists
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Convert to dictionary format
    result = order.to_dict()

    return jsonify(result)


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    # Get user ID from token
    token = request.headers.get('Authorization').split()[1]
    payload = jwt.decode(token, app.config['SECRET_KEY'])
    user_id = payload['user_id']

    # Create a new order
    new_order = Order(user_id=user_id)
    db.session.add(new_order)

    # Add order items
    for item in data['items']:
        product = Product.query.get(item['product_id'])

        # Check if product exists
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Check if product is available
        if product.availability < item['quantity']:
            return jsonify({'error': 'Product not available'}), 400

        # Create a new order item
        new_item = OrderItem(order=new_order, product=product, quantity=item['quantity'])
        db.session.add(new_item)

        # Update product availability
        product.availability -= item['quantity']

    db.session.commit()

    return jsonify(new_order.to_dict()), 201


@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()

    # Get order by ID
    order = Order.query.get(order_id)

    # Check if order exists
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Update order items
    for item in data['items']:
        order_item = OrderItem.query.filter_by(order_id=order_id, product_id=item['product_id']).first()

        # Check if order item exists
        if not order_item:
            return jsonify({'error': 'Order item not found'}), 404

        # Check if product is available
        product = Product.query.get(item['product_id'])
        if product.availability + order_item.quantity < item['quantity']:
            return jsonify({'error': 'Product not available'}), 400

        # Update order item quantity
        order_item.quantity = item['quantity']

        # Update product availability
        product.availability += order_item.quantity - item['quantity']

    db.session.commit()

    return jsonify(order.to_dict())


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Get order by ID
    order = Order.query.get(order_id)

    # Check if order exists
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Delete order items
    for item in order.order_items:
        product = Product.query.get(item.product_id)
        product.availability += item.quantity
        db.session.delete(item)

    # Delete order
    db.session.delete(order)
    db.session.commit()

    return '', 204

## TODO::INVENTORY MANAGEMENT

@app.route('/inventory', methods=['GET'])
def inventory():
    # Get all products with inventory data
    products = Product.query.all()

    # Convert to dictionary format
    result = [product.to_dict() for product in products]

    return jsonify(result)


@app.route('/inventory/<int:product_id>', methods=['GET'])
def get_inventory(product_id):
    # Get product by ID
    product = Product.query.get(product_id)

    # Check if product exists
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Get inventory data for the product
    inventory = Inventory.query.filter_by(product_id=product_id).all()

    # Convert to dictionary format
    result = product.to_dict()
    result['inventory'] = [i.to_dict() for i in inventory]

    return jsonify(result)


@app.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.get_json()

    # Get product by ID
    product = Product.query.get(data['product_id'])

    # Check if product exists
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Create a new inventory entry
    new_inventory = Inventory(product_id=data['product_id'], quantity=data['quantity'], timestamp=datetime.utcnow())
    db.session.add(new_inventory)
    db.session.commit()

    return jsonify(new_inventory.to_dict()), 201


@app.route('/inventory/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    data = request.get_json()

    # Get inventory entry by ID
    inventory = Inventory.query.get(inventory_id)

    # Check if inventory entry exists
    if not inventory:
        return jsonify({'error': 'Inventory entry not found'}), 404

    # Update inventory data
    inventory.quantity = data['quantity']
    inventory.timestamp = datetime.utcnow()
    db.session.commit()

    return jsonify(inventory.to_dict())


@app.route('/inventory/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    # Get inventory entry by ID
    inventory = Inventory.query.get(inventory_id)

    # Check if inventory entry exists
    if not inventory:
        return jsonify({'error': 'Inventory entry not found'}), 404

    # Delete inventory entry
    db.session.delete(inventory)
    db.session.commit()

    return '', 204




if __name__ == '__main__':
    app.run(debug=True)