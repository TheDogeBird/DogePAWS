import asyncpg
from main import pool
from asyncpg.pool import Pool

class User:
    def __init__(self, id, email, password, role, is_admin=False, is_sub_admin=False):
        self.id = id
        self.email = email
        self.password = password
        self.role = role
        self.is_admin = is_admin
        self.is_sub_admin = is_sub_admin

    def is_manager(self):
        return self.role == 'manager'

    def is_teamlead(self):
        return self.role == 'teamlead'

    def is_employee(self):
        return self.role == 'employee'

    def is_customer(self):
        return self.role == 'customer'

    def is_vendor(self):
        return self.role == 'vendor'


async def get_pool():
    pool = await asyncpg.create_pool(
        host='localhost',
        port=5432,
        user='postgres',
        password='mysecretpassword',
        database='mydatabase'
    )
    return pool

async def get_user_by_email(email):
    async with pool.acquire() as conn:
        user = await conn.fetchrow('SELECT * FROM users WHERE email=$1', email)
        if user:
            return User(user['id'], user['email'], user['password'], user['role'], user['is_admin'], user['is_sub_admin'])
        else:
            return None


async def authenticate(request, email, password):
    user = await get_user_by_email(email)
    if user and password == user.password:
        return user
    else:
        return None


async def add_user(email, password, role, is_admin=False, is_sub_admin=False):
    async with pool.acquire() as conn:
        await conn.execute('INSERT INTO users (email, password, role, is_admin, is_sub_admin) VALUES ($1, $2, $3, $4, $5)', email, password, role, is_admin, is_sub_admin)

async def remove_user(email):
    async with pool.acquire() as conn:
        await conn.execute('DELETE FROM users WHERE email=$1', email)


async def retrieve_user(request, payload, *args, **kwargs):
    user_id = payload.get('user_id', None)
    if user_id:
        return await get_user_by_email(user_id)
    return None
