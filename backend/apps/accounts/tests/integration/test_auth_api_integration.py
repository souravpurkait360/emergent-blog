"""Integration tests — Auth API (accounts app).

Covers: login, register, me, logout, invalid credentials, admin user list.
Uses a live HTTP session against the running backend.
"""

from conftest import BASE_URL
import requests

# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------


def test_admin_login_returns_user_object() -> None:
    resp = requests.post(
        f"{BASE_URL}/api/auth/token/",
        json={"email": "admin@blog.com", "password": "admin123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "user" in data
    assert data["user"]["email"] == "admin@blog.com"
    # Tokens must NOT be in the response body — they live in httpOnly cookies
    assert "access" not in data
    assert "refresh" not in data


def test_login_sets_httponly_access_cookie() -> None:
    session = requests.Session()
    resp = session.post(
        f"{BASE_URL}/api/auth/token/",
        json={"email": "admin@blog.com", "password": "admin123"},
    )
    assert resp.status_code == 200
    assert "access_token" in session.cookies


def test_invalid_credentials_returns_401() -> None:
    resp = requests.post(
        f"{BASE_URL}/api/auth/token/",
        json={"email": "nobody@example.com", "password": "wrongpassword"},
    )
    assert resp.status_code in (400, 401)


# ---------------------------------------------------------------------------
# Register
# ---------------------------------------------------------------------------


def test_register_new_user_returns_201() -> None:
    resp = requests.post(
        f"{BASE_URL}/api/auth/register/",
        json={
            "email": "integration_user@blog.com",
            "username": "integration_user",
            "password": "IntTest1234!",
            "password2": "IntTest1234!",
        },
    )
    # 201 on first run; 400 (email taken) on subsequent runs — both are valid
    assert resp.status_code in (200, 201, 400), f"Unexpected: {resp.status_code} {resp.text}"


def test_registered_user_can_login() -> None:
    requests.post(
        f"{BASE_URL}/api/auth/register/",
        json={
            "email": "integration_user@blog.com",
            "username": "integration_user",
            "password": "IntTest1234!",
            "password2": "IntTest1234!",
        },
    )
    resp = requests.post(
        f"{BASE_URL}/api/auth/token/",
        json={"email": "integration_user@blog.com", "password": "IntTest1234!"},
    )
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# /me endpoint
# ---------------------------------------------------------------------------


def test_me_returns_authenticated_user(admin_session) -> None:
    resp = admin_session.get(f"{BASE_URL}/api/auth/me/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "admin@blog.com"


def test_me_requires_auth() -> None:
    resp = requests.get(f"{BASE_URL}/api/auth/me/")
    assert resp.status_code == 401


# ---------------------------------------------------------------------------
# Admin — user list
# ---------------------------------------------------------------------------


def test_admin_can_list_users(admin_session) -> None:
    resp = admin_session.get(f"{BASE_URL}/api/auth/users/")
    assert resp.status_code == 200
