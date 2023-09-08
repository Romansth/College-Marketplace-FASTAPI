import pytest
from app import schemas

def test_get_all_listings(authorized_client, test_listings):
    res = authorized_client.get("/listings/")

    def validate(listing):
        return schemas.Listing(**listing)
    listings_map = map(validate, res.json())
    listings_list = list(listings_map)

    assert len(res.json()) == len(test_listings)
    assert res.status_code == 200

def test_get_one_listing_not_exist(authorized_client, test_listings):
    res = authorized_client.get(f"/listings/88888")
    assert res.status_code == 404

def test_get_one_listing(authorized_client, test_listings):
    res = authorized_client.get(f"/listings/{test_listings[0].product_id}")
    response_data = res.json()
    assert response_data['name'] == test_listings[0].name
    assert response_data['description'] == test_listings[0].description

def test_create_listing(authorized_client, test_user, test_listings):
    res = authorized_client.post(
        "/listings/", json={
            "name": "bottle",
            "description": "graduating soon so selling it",
            "price": 30,
            "quantity": 2,
            "condition": "new",
            "user_id": test_listings[0].user_id
    })
    created_listing = schemas.Listing(**res.json())
    assert res.status_code == 201
    assert created_listing.name == "bottle"
    assert created_listing.description == "graduating soon so selling it"
    assert created_listing.price == 30
    assert created_listing.user_id == test_user['user_id']


def test_unauthorized_user_create_listing(client, test_user, test_listings):
    res = client.post(
        "/listings/", json={
            "name": "bottle",
            "description": "graduating soon so selling it",
            "price": 30,
            "quantity": 2,
            "condition": "new",
            "user_id": test_listings[0].user_id
    })
    assert res.status_code == 401


def test_unauthorized_user_delete_listing(client, test_user, test_listings):
    res = client.delete(
        f"/listings/{test_listings[0].product_id}")
    assert res.status_code == 401


def test_delete_listing_success(authorized_client, test_user, test_listings):
    res = authorized_client.delete(
        f"/listings/{test_listings[0].product_id}")

    assert res.status_code == 204


def test_delete_listing_non_exist(authorized_client, test_user, test_listings):
    res = authorized_client.delete(
        f"/listings/8000000")

    assert res.status_code == 404


def test_delete_other_user_listing(authorized_client, test_user, test_listings):
    res = authorized_client.delete(
        f"/listings/{test_listings[3].product_id}")
    assert res.status_code == 403


def test_update_listing(authorized_client, test_user, test_listings):
    data = {
            "name": "updated bottle",
            "description": "graduating soon so selling it",
            "price": 30,
            "quantity": 2,
            "condition": "new",
            "user_id": test_listings[0].user_id
    }
    res = authorized_client.put(f"/listings/{test_listings[0].user_id}", json=data)
    updated_listing = schemas.Listing(**res.json())
    assert res.status_code == 200
    assert updated_listing.name == data['name']
    assert updated_listing.price == data['price']


def test_update_other_user_listing(authorized_client, test_user, test_user2, test_listings):
    data = {
            "name": "updated bottle",
            "description": "graduating soon so selling it",
            "price": 30,
            "quantity": 2,
            "condition": "new",
            "user_id": test_listings[0].user_id
    }
    res = authorized_client.put(f"/listings/{test_listings[3].product_id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_listing(client, test_user, test_listings):
    res = client.put(
        f"/listings/{test_listings[0].product_id}")
    assert res.status_code == 401


def test_update_listing_non_exist(authorized_client, test_user, test_listings):
    data = {
            "name": "updated bottle",
            "description": "graduating soon so selling it",
            "price": 30,
            "quantity": 2,
            "condition": "new",
            "user_id": test_listings[0].user_id
    }
    res = authorized_client.put(
        f"/listings/8000000", json=data)

    assert res.status_code == 404