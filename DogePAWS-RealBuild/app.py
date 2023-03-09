# app.py

import sanic_jwt
from sanic import Sanic, request, response
from sanic.response import file, html, redirect
from werkzeug.exceptions import HTTPException
from sanic_jwt import initialize, exceptions, Authentication
from Utils import validate_request_payload, retrieve_payload
from UserMgmt import User, get_user_by_username, add_user, remove_user, retrieve_user
import config
from routes import setup_routes

import os
import jwt
import logging

logging.getLogger().disabled = False

app = Sanic("DogePAWS")
app.config['SANIC_JWT_SECRET'] = 'secret'


async def before_server_start(app, loop):
    try:
        await app.auth.extract_jwt_token(request)
    except exceptions.AuthenticationFailed:
        # Redirect to the login page
        return response.redirect('/login')

    # Set up the routes
    setup_routes()


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

if __name__ == '__main__':
    app.run(debug=True)
