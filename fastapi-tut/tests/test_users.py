from collections.abc import Generator

from fastapi.testclient import TestClient
import pytest
from app.dependencies import get_user_repository
from app.main import app
from app.storage import active_users


# @pytest.fixture(autouse=True)
# def setup_function():
#     active_users.clear()


class FakeUserRepository:
    def create_user(self, user):
        return {
            "id": 1,
            "name": user.name,
            "age": user.age
        }
    
def override_user_repo():
    return FakeUserRepository()

@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_user_repository] = override_user_repo
    
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_root(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_user_hides_password(client: TestClient):
    response = client.post(
        "/users",
        json={
            "name": "Auco",
            "age": 21,
            "password": "secret123",
        },
    )


    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Auco",
        "age": 21,
    }
    assert "password" not in response.json()


def test_list_users(client: TestClient):
    client.post(
        "/users",
        json={
            "name": "Auco",
            "age": 21,
            "password": "secret",
        },
    )

    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Auco",
            "age": 21,
        }
    ]


def test_get_user_by_id(client: TestClient):
    client.post(
        "/users",
        json={
            "name": "Auco",
            "age": 21,
            "password": "secret",
        },
    )

    response = client.get("/users/0")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Auco",
        "age": 21,
    }


def test_get_user_by_invalid_id_returns_404(client: TestClient):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_user_preserves_password_and_hides_it(client: TestClient):
    client.post(
        "/users",
        json={
            "name": "Auco",
            "age": 21,
            "password": "secret",
        },
    )

    response = client.put(
        "/users/0",
        json={
            "name": "Updated Auco",
            "age": 22,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "name": "Updated Auco",
        "age": 22,
    }
    assert active_users[0].password == "secret"


def test_patch_user_updates_only_sent_fields(client: TestClient):
    client.post(
        "/users",
        json={
            "name": "Auco",
            "age": 21,
            "password": "secret",
        },
    )

    response = client.patch(
        "/users/0",
        json={
            "age": 22,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "name": "Auco",
        "age": 22,
    }
    assert active_users[0].password == "secret"


def test_delete_user(client: TestClient):
    client.post(
        "/users",
        json={
            "name": "Auco",
            "age": 21,
            "password": "secret",
        },
    )

    response = client.delete("/users/0")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Auco",
        "age": 21,
    }

    assert active_users == []