from sanic import response
from sanic.views import HTTPMethodView
#from sanic.exceptions import abort
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sanic_jwt import protected
from app import app
from app import app
from UserMgmt import User, get_user_by_email, add_user, remove_user, authenticate, retrieve_user
import jwt


env = Environment(
    loader=FileSystemLoader('Views'),
    autoescape=select_autoescape(['html', 'xml'])
)


class BaseView(HTTPMethodView):
    async def render(self, request, template_name, **context):
        template = env.get_template(template_name)
        html = template.render(request=request, **context)
        return html


class LoginView(BaseView):
    async def get(self, request):
        return await self.render(request, 'login.html')

    async def post(self, request):
        email = request.form.get('email')
        password = request.form.get('password')
        user = await authenticate(request, email, password)
        if user:
            payload = {'user_id': user.email}
            token = jwt.encode(payload, app.config.SANIC_JWT_SECRET, algorithm='HS256')
            headers = {'Authorization': 'Bearer {}'.format(token)}
            if user.is_admin or user.is_sub_admin:
                return await response.file('views/dashboard.html', headers=headers)
            elif user.is_employee:
                return await response.file('views/employee_dashboard.html', headers=headers)
        else:
            return response.redirect('/login')


class DashboardView(BaseView):
    @protected()
    async def get(self, request):
        user = await retrieve_user(request, request.app.config.SANIC_JWT_SECRET)
        if user.is_admin or user.is_sub_admin:
            return await self.render(request, 'dashboard.html')
        else:
            return response.redirect('/login')


class EmployeeDashboardView(BaseView):
    @protected()
    async def get(self, request):
        user = await retrieve_user(request, request.app.config.SANIC_JWT_SECRET)
        if user.is_employee:
            return await self.render(request, 'employee_dashboard.html')
        else:
            return response.redirect('/login')
