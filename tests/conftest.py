import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_project(client):
    response = client.post(
        "/api/v1/projects",
        json={"name": "Website Redesign", "description": "Full redesign of the marketing site"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def sample_task(client, sample_project):
    response = client.post(
        f"/api/v1/projects/{sample_project['id']}/tasks",
        json={"title": "Design homepage mockup", "priority": "high", "assignee_name": "Riya"},
    )
    assert response.status_code == 201
    return response.json()