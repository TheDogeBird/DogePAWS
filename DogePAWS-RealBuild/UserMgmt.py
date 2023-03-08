import asyncpg
from connection import create_pool
from asyncpg.pool import Pool

class User:
    def __init__(self, id, username, password, role, is_admin=False, is_sub_admin=False):
        self.id = id
        self.username = username
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


async def get_user_by_username(username):
    async with create_pool() as pool:
        async with pool.acquire() as conn:
            user = await conn.fetchrow('SELECT * FROM users WHERE username=$1', username)
            if user:
                return User(user['id'], user['username'], user['password'], user['role'], user['is_admin'], user['is_sub_admin'])
            else:
                return None


async def authenticate(request, username, password):
    user = await get_user_by_username(username)
    if user and password == user.password:
        return user
    else:
        return None


async def add_user(username, password, role, is_admin=False, is_sub_admin=False):
    async with create_pool() as pool:
        async with pool.acquire() as conn:
            await conn.execute('INSERT INTO users (username, password, role, is_admin, is_sub_admin) VALUES ($1, $2, $3, $4, $5)', username, password, role, is_admin, is_sub_admin)

async def remove_user(username):
    async with create_pool() as pool:
        async with pool.acquire() as conn:
            await conn.execute('DELETE FROM users WHERE username=$1', username)


async def retrieve_user(request, payload, *args, **kwargs):
    user_id = payload.get('user_id', None)
    if user_id:
        return await get_user_by_username(user_id)
    return None
