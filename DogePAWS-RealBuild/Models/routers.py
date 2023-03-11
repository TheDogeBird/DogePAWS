from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash
from Models.database import SessionLocal
from Models.user import User, get_user_by_email, verify_password

router = APIRouter()
login_router = APIRouter()

security = HTTPBasic()

@login_router.post("/login")
def login(credentials: HTTPBasicCredentials, db: Session = Depends(SessionLocal)):
    user = get_user_by_email(credentials.username, db)
    if user is None or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Logged in successfully"}

@router.post("/login")
def login(credentials: HTTPBasicCredentials, db: Session = Depends(SessionLocal)):
    user = db.query(User).filter(User.email.ilike(credentials.username)).first()
    if user is None or not check_password_hash(user.password_hash, credentials.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Logged in successfully"}
