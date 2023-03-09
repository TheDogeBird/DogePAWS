#config.py

from sanic import Sanic
from connection import create_pool

app = Sanic(__name__)

@app.listener("before_server_start")
async def setup_db(app, loop):
    app.pool = await create_pool(app.config["DATABASE_CONFIG"])

@app.listener("after_server_stop")
async def close_db(app, loop):
    await app.pool.close()
