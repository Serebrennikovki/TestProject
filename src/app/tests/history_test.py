from unittest.mock import patch

from fastapi.testclient import TestClient

from models.enums import TaskStatus, TransactionStatus, TransactionType

def test_get_history_success(client: TestClient):
    user_login = "test"
    response = client.get(f"/api/history/{user_login}")
    print("response = ")
    print(response.json())
    answer = response.json()
    first_operation = answer[0]
    second_operation = answer[1]
    assert first_operation['type'] == TransactionType.Debit.value
    assert first_operation['cost'] == '10'
    assert first_operation['status'] == TransactionStatus.Done.value
    assert second_operation['type'] == TransactionType.Credit.value
    assert second_operation['cost'] == '20'
    assert second_operation['status'] == TransactionStatus.Canceled.value
    assert response.status_code == 200

def test_get_history_no_exist_user_error(client: TestClient):
    user_login = "test1"
    response = client.get(f"/api/history/{user_login}")
    assert response.status_code == 404

def test_get_history_prediction(client: TestClient):
    login = "test"
    data = "тестовый запрос"
    payload = {
        "user_login": login,
        "input_data": data
    }

    with patch("services.business_logic.prediction.send_to_queue"):
        task = client.post("/api/predict/add", json=payload)
    response = client.get(f"/api/predict/{login}")
    answer = response.json()[0]
    assert data == answer['input_data']
    assert TaskStatus.Waiting.value == answer['status']
    assert response.status_code == 200