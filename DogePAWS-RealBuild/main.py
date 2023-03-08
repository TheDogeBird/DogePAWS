from sanic import Sanic
from connection import create_pool
import config

app = Sanic(__name__)
app.config.SANIC_JWT_SECRET = config.SANIC_JWT_SECRET

# connection pool stuff
pool = None

@app.listener('before_server_start')
async def setup_db(app, loop):
    global pool
    pool = await create_pool()

from routes import *

if __name__ == '__main__':
    app.run()
