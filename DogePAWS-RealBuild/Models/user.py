# Models/users.py
from typing import List
from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from Models.database import Base
from sqlalchemy.orm import Session

is_admin = Column(Boolean, nullable=False, default=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

def get_user_by_email(email: str, session: Session) -> User:
    return session.query(User).filter(User.email.ilike(email)).first()


def get_user_by_id(user_id: int, session: Session) -> User:
    return session.query(User).filter(User.id == user_id).first()


def get_users(session: Session) -> List[User]:
    return session.query(User).all()

def verify_password(self, password):
    return check_password_hash(self.password_hash, password)


def create_user(user: User, session: Session):
    user.is_admin = False  # set the is_admin attribute to False by default
    session.add(user)
    session.flush()
    session.refresh(user)


def update_user(user: User, session: Session):
    db_user = session.query(User).filter(User.id == user.id).first()
    db_user.username = user.username
    db_user.password_hash = user.password_hash
    db_user.is_admin = user.is_admin
    session.commit()


def delete_user(user_id: int, session: Session):
    session.query(User).filter(User.id == user_id).delete()
    session.commit()
