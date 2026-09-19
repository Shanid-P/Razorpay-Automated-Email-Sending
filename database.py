# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base

# DATABASE_URL = "sqlite:///database.db"

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )

# Base = declarative_base()

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# def get_db():

#     db = SessionLocal()

#     try:
#         yield db

#     finally:
#         db.close()


import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()