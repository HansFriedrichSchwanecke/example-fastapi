import time

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:' \
                          f'{settings.database_password}@' \
                          f'{settings.database_hostname}/' \
                          f'{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()


# DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:

    try:
        conn = psycopg2.connect(host=settings.database_hostname,
                                database=settings.database_name,
                                user=settings.database_username,
                                password=settings.database_password,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()

        print("Database connection was successful")
        break
    except Exception as error:
        print("Failed database connection")
        print("Error: ", error)

    time.sleep(2)
