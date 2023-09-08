from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "test@gmail.com", "password": "test", "first_name": "Roman", "last_name": "Shrestha", "class_year": 2026}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "test1@gmail.com", "password": "test1", "first_name": "Tom", "last_name": "Riddle", "class_year": 2026}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['user_id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_listings(test_user, session, test_user2):
    listings_data = [{
        "name": "bottle",
        "description": "graduating soon so selling it",
        "price": 30,
        "quantity": 2,
        "condition": "new",
        "user_id": test_user["user_id"]
    }, {
        "name": "pen",
        "description": "graduating soon so selling it",
        "price": 50,
        "quantity": 3,
        "condition": "old",
        "user_id": test_user["user_id"]
    },{
        "name": "book",
        "description": "graduating soon so selling it",
        "price": 30,
        "quantity": 2,
        "condition": "new",
        "user_id": test_user["user_id"]
    }, {
        "name": "fridge",
        "description": "graduating soon so selling it",
        "price": 30,
        "quantity": 2,
        "condition": "new",
        "user_id": test_user2["user_id"]
    }]

    def create_listing_model(listing):
        return models.Listing(**listing)

    listing_map = map(create_listing_model, listings_data)
    listings = list(listing_map)

    session.add_all(listings)
    session.commit()

    listings = session.query(models.Listing).all()
    return listings

@pytest.fixture
def test_order(test_listings, session, test_user, test_user2):
    new_order = models.Order(
    product_id= test_listings[0].product_id,
    cost= 30,
    status= "pending",
    quantity= 1,
    buyer_id= test_user2["user_id"],
    seller_id= test_user["user_id"],
    )
    session.add(new_order)
    session.commit()
