from fastapi import FastAPI
from Models.routers import login_router

app = FastAPI()

# Mount the login router at /login
app.include_router(login_router, prefix="/login")
