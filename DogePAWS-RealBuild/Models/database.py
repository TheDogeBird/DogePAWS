from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from contextlib import contextmanager
from config import settings


# Replace DB_NAME, DB_USER, DB_PASSWORD with your actual database credentials
DATABASE_URL = f"postgresql://{settings['db_user']}:{settings['db_password']}@localhost/{settings['db_name']}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a session factory
SessionFactory = sessionmaker(bind=engine)

# Create a scoped session factory
Session = scoped_session(SessionFactory)

Base = declarative_base()

# Declare the db object
db = Session()