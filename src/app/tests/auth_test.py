from fastapi.testclient import TestClient

def test_signup_success(client: TestClient):
    payload = {
        "login": "test_user",
        "password": "123456",
        "name": "Test"
    }

    response = client.post("/api/auth/signup", json=payload)

    assert response.status_code == 201
    assert response.json() == {"message": "User successfully registered"}

def test_signup_when_login_exist_error(client: TestClient):
    payload = {
        "login": "test",
        "password": "test",
        "name": "test"
    }

    response = client.post("/api/auth/signup", json=payload)

    assert response.status_code == 409
    assert response.json() == {"detail": "User with this login already exists"}


def test_signin_success(client: TestClient):
    payload = {
            "login": "test",
            "password": "test"
        }
        
    response = client.post("/api/auth/signin", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": "User successfully logged in"}


def test_signup_when_login_doesnt_exist_error(client: TestClient):
    payload = {
        "login": "test1",
        "password": "test",
    }

    response = client.post("/api/auth/signin", json=payload)

    assert response.status_code == 404

def test_signup_when_password_incorrect_error(client: TestClient):
    payload = {
        "login": "test",
        "password": "test12",
    }

    response = client.post("/api/auth/signin", json=payload)

    assert response.status_code == 401
    assert response.json() == {"detail":"Incorrect password"}