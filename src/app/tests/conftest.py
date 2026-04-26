import pytest
from fastapi.testclient import TestClient
from api import app
from sqlmodel import SQLModel, Session, create_engine 
from tests.test_data import add_test_data
from database.database import get_session 
from sqlalchemy.pool import StaticPool
from core.authenticate import authenticate_cookie

@pytest.fixture(name="session")  
def session_fixture():  
    url = 'postgresql+psycopg://user:password@localhost:5432/app'
    engine = create_engine(url)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        add_test_data(session)
        yield session

@pytest.fixture(name="client") 
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    app.dependency_overrides[get_session] = get_session_override  
    app.dependency_overrides[authenticate_cookie] = lambda: "test"  
    
    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear()

