from sanic import response
from sanic_jwt import exceptions

from app import app
from routes import setup_routes
from middlewares import check_authentication

app.register_middleware(check_authentication)
setup_routes(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
