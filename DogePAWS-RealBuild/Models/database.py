from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from config import settings


# Replace DB_NAME, DB_USER, DB_PASSWORD with your actual database credentials
DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)

# Create a session factory
SessionFactory = sessionmaker(bind=engine)

# Create a scoped session factory
Session = scoped_session(SessionFactory)

session_factory = sessionmaker(bind=engine)


db = Session()

engine = create_engine(DATABASE_URL)
Base = declarative_base()




@contextmanager
def get_db():
    try:
        yield Session
    finally:
        Session.remove()
