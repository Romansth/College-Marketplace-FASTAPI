import pytest

def test_create_order(authorized_client, test_listings):
    res = authorized_client.post("/order/", json = {
    "product_id": test_listings[0].product_id,
    "quantity": 1,
    }) 
    assert res.status_code == 201

def test_create_order_unauthorized(client, test_listings):
    res = client.post("/order/", json = {
    "product_id": test_listings[0].product_id,
    "quantity": 1,
    }) 
    assert res.status_code == 401

def test_create_order_bad_order(authorized_client, test_listings):
    res = authorized_client.post("/order/", json = {
    "product_id": test_listings[0].product_id,
    "quantity": 4,
    }) 
    assert res.status_code == 400

def test_change_order_status(authorized_client, test_order):
    res = authorized_client.put(f"/order/1", json = {"status": "closed"})
    assert res.status_code == 200

def test_change_order_status_unauthorized(client, test_order):
    res = client.put(f"/order/1", json = {"status": "closed"})
    assert res.status_code == 401