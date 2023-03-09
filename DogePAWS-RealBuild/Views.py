# Views.py

from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import html
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('Views', '.'),
    autoescape=select_autoescape(['html', 'xml'])
)

views = Blueprint('views')

@views.route('/')
async def index(request):
    template = env.get_template('login.html')
    return html(template.render())


@views.route('/dashboard')
async def dashboard(request):
    template = env.get_template('dashboard.html')
    return html(template.render())


@views.route('/employee_dashboard')
async def employee_dashboard(request):
    template = env.get_template('employee_dashboard.html')
    return html(template.render())

class LoginView(HTTPMethodView):
    async def get(self, request):
        return html('<h1>Login page</h1>')

    async def post(self, request):
        username = request.form.get('username')
        password = request.form.get('password')
        if await self.authenticate(username, password):
            return html('<h1>Logged in successfully!</h1>')
        else:
            return html('<h1>Invalid username or password</h1>')

    async def authenticate(self, username, password):
        # Your authentication logic here
        if username == 'admin' and password == 'password':
            return True
        else:
            return False
