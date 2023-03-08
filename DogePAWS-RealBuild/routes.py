from sanic import response
from sanic_jwt import exceptions, initialize, protected, inject_user
from main import app
from UserMgmt import User, get_user_by_email, add_user, remove_user, authenticate, retrieve_user
import jwt

@app.route('/')
async def index(request):
    return response.redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = await authenticate(request, email, password)
        if user:
            payload = {'user_id': user.email}
            token = jwt.encode(payload, app.config.SANIC_JWT_SECRET, algorithm='HS256')
            headers = {'Authorization': 'Bearer {}'.format(token)}
            if user.is_admin or user.is_sub_admin:
                return response.redirect('/dashboard', headers=headers)
            elif user.is_employee:
                return response.redirect('/employee-dashboard', headers=headers)
        else:
            return response.redirect('/login')

    return await response.file('templates/login.html')


@app.route('/dashboard')
@protected()
async def dashboard(request):
    user = await retrieve_user(request, request.app.config.SANIC_JWT_SECRET)
    if user.is_admin or user.is_sub_admin:
        return await response.file('templates/dashboard.html')
    else:
        return response.redirect('/login')


@app.route('/employee-dashboard')
@protected()
async def employee_dashboard(request):
    user = await retrieve_user(request, request.app.config.SANIC_JWT_SECRET)
    if user.is_employee:
        return await response.file('templates/employee-dashboard.html')
    else:
        return response.redirect('/login')
