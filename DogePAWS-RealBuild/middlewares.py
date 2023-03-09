# Middlewares.py

from sanic import Blueprint, response
from sanic_jwt import exceptions
from sanic_jinja2 import SanicJinja2

from UserMgmt import authenticate

jinja = SanicJinja2()

bp = Blueprint('auth')


@bp.middleware('request')
async def check_authentication(request):
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        # your authentication code here
        user = await authenticate(request, username, password)

        # define the authenticated_user attribute in the ctx object
        request.app.ctx.authenticated_user = user

    except exceptions.AuthenticationFailed:
        return response.redirect('/login')

    except Exception as e:
        # handle other exceptions here
        return response.json({'message': f'Error: {str(e)}'}, status=500)


@bp.route('/login')
async def login(request):
    return jinja.render('login.html')


@bp.route('/protected')
async def protected(request):
    return response.json({'message': 'You are authorized'})
