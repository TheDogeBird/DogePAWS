# Routes.py

from sanic import Blueprint
from Views import LoginView
from sanic.response import html
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('Views', '.'),
    autoescape=select_autoescape(['html', 'xml'])
)

auth = Blueprint('auth', url_prefix='/auth')
auth.add_route(LoginView.as_view(), '/login')

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

def setup_routes(app):
    app.blueprint(auth)
    app.blueprint(views)