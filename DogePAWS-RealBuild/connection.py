# connection.py

import asyncpg

async def create_pool():
    pool = await asyncpg.create_pool(
        user='DogePAWS',
        password='DogePAWS!',
        database='pos_db',
        host='localhost',
        port=5432  # replace with your port number
    )
    return pool

async def get_pool():
    return await create_pool()
