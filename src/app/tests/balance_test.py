from fastapi.testclient import TestClient

def test_get_balance_success(client: TestClient):
    user_login = "test"
    response = client.get(f"/api/balance/{user_login}")

    assert response.status_code == 200
    assert response.json() == "10"

def test_get_balance_when_user_not_exist_validation_error(client: TestClient):
    user_login = "test1"
    response = client.get(f"/api/balance/{user_login}")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_add_deposit_error_dont_exist_amount(client: TestClient):
    payload = {
        "user_login": "test",
        "deposit": 10,
    }
    response = client.post(f"/api/balance/deposit", json=payload)
    assert response.status_code == 422


def test_add_deposit_success(client: TestClient):
    payload = {
        "user_login": "test",
        "amount": 10,
    }
    response = client.post(f"/api/balance/deposit", json=payload)
    assert response.status_code == 200
    assert response.json() == "20"
