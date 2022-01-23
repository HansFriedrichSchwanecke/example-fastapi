from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app

from app.config import settings
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:' \
                          f'{settings.database_password}@' \
                          f'{settings.database_hostname}/' \
                          f'{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)


@fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@fixture
def client(session):
    print("my session fixture ran")
    # Before test runs
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # After test runs


@fixture
def test_user(client):
    user_data = {"email": "hello1352@mytum.de",
                 "password": "password123"}

    res = client.post("/users", json=user_data)

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user