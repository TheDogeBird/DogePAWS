import sanic_jwt
from sanic import Sanic
from sanic.response import file, html, redirect
from werkzeug.exceptions import HTTPException
from sanic_jwt import initialize, exceptions, Authentication
from Utils import validate_request_payload, retrieve_payload
from UserMgmt import User, get_user_by_username, add_user, remove_user, retrieve_user
import config

import os
import jwt

app = Sanic("DogePAWS")

app.config['SANIC_JWT_SECRET'] = 'secret'


class CustomAuthenticate(Authentication):
    def __init__(self, app, config):
        super().__init__(app, config)

    async def authenticate(self, request, *args, **kwargs):
        username = request.form.get('username')
        password = request.form.get('password')

        user = await get_user_by_username(username)

        if user and self.verify_password(user, password):
            return user

    def verify_password(self, user, password):
        return password == user.password


auth = CustomAuthenticate(app, app.config)
initialize(app, authenticate=auth)

app.static('/static', './static')

@app.route('/')
async def index(request):
    return await file('./Views/login.html')

@app.route('/dashboard')
@sanic_jwt.protected()
async def dashboard(request):
    user = await retrieve_user(request, app.config.SANIC_JWT_SECRET)
    if user.is_admin or user.is_sub_admin:
        return await file('./Views/dashboard.html')
    else:
        return redirect('/')

@app.route('/employee-dashboard')
@sanic_jwt.protected()
async def employee_dashboard(request):
    user = await retrieve_user(request, app.config.SANIC_JWT_SECRET)
    if user.is_employee:
        return await file('./Views/employee_dashboard.html')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

