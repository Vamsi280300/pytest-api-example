import pytest
import api_helpers


# Validating  PATCH updates order status successfully
def test_patch_order_by_id():
    order_id = 1
    test_endpoint = f"/store/order/{order_id}"

    payload = {"status": "delivered"}

    response = api_helpers.patch_api_data(test_endpoint, payload)
    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Order and pet status updated successfully"
    assert data["status"] == "delivered"
    assert "id" in data
    assert isinstance(data["id"], int)


# Validating API rejects invalid payload
def test_patch_order_invalid_payload():
    order_id = 2
    test_endpoint = f"/store/order/{order_id}"

    payload = {"status": 123}

    response = api_helpers.patch_api_data(test_endpoint, payload)
    assert response.status_code in [400, 422]


# Validating PATCH on non-existing order returns 404
def test_patch_order_not_found():
    order_id = 999
    test_endpoint = f"/store/order/{order_id}"

    payload = {"status": "delivered"}

    response = api_helpers.patch_api_data(test_endpoint, payload)
    assert response.status_code == 404


# Validating PATCH persists changes
def test_patch_order_persistence():
    order_id = 1
    test_endpoint = f"/store/order/{order_id}"

    payload = {"status": "processing"}

    patch_response = api_helpers.patch_api_data(test_endpoint, payload)
    assert patch_response.status_code == 200

    get_response = api_helpers.get_api_data(test_endpoint)
    assert get_response.status_code == 200

    assert get_response.json()["status"] == "processing"