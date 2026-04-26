from decimal import Decimal

from fastapi.testclient import TestClient
from unittest.mock import patch
from models.balance import Balance
from models.user import User

from sqlmodel import Session

def test_add_predict_success(session: Session, client: TestClient):
    payload = {
        "user_login": "test",
        "input_data": "тестовый запрос"
    }

    user: User = session.query(User).filter_by(login = 'test').first()
    initial_balance: Decimal = session.query(Balance).filter_by(user_id = user.id).first().balance
    with patch("services.business_logic.prediction.send_to_queue") as mock_send:
        response = client.post("/api/predict/add", json=payload)
        mock_send.assert_called_once()  
    balance: Balance = session.query(Balance).filter_by(user_id = user.id).first()
    expected_balance = initial_balance - Decimal(5)
    assert balance.balance == expected_balance
    assert response.status_code == 201

def test_add_predict_incorrect_request_error(client: TestClient):
    payload = {
        "user_login": "test",
        "input_data": ""
    }
  
    with patch("services.business_logic.prediction.send_to_queue") as mock_send:
        response = client.post("/api/predict/add", json=payload)
    assert response.status_code == 422