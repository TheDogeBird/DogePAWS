import os
from sanic import response
from sanic.views import HTTPMethodView
from UserMgmt import User, get_user_by_username, add_user, remove_user, retrieve_user
from sanic_jwt.decorators import protected
from Views import LoginView, DashboardView, EmployeeDashboardView
from app import app

def setup_routes():
    app.add_route(LoginView.as_view(), '/login')
    app.add_route(DashboardView.as_view(), '/dashboard')
    app.add_route(EmployeeDashboardView.as_view(), '/employee-dashboard')

    base_dir = os.path.dirname(os.path.abspath(__file__))

    login_view = LoginView()
    dashboard_view = DashboardView()
    employee_dashboard_view = EmployeeDashboardView()

    from sanic.response import html

    @app.route('/')
    async def index(request):
        with open("Views/login.html", "r") as f:
            html_str = f.read()
        return html(html_str)

    @app.route("/login")
    async def login(request):
        with open("Views/login.html", "r") as f:
            html = f.read()
        return response.html(html)

    @app.route('/dashboard')
    @protected()
    async def dashboard(request):
        user = await retrieve_user(request, app.config.SANIC_JWT_SECRET)
        if user.is_admin or user.is_sub_admin:
            return await dashboard_view.render(request=request, template_name='dashboard.html')
        else:
            return response.redirect('/login')

    @app.route('/employee-dashboard')
    @protected()
    async def employee_dashboard(request):
        user = await retrieve_user(request, app.config.SANIC_JWT_SECRET)
        if user.is_employee:
            return await employee_dashboard_view.render(request=request, template_name='employee_dashboard.html')
        else:
            return response.redirect('/login')

