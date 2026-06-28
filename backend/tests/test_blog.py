"""Backend API tests for INKFLOW blog app"""

import os

import pytest
import requests


def _get_base_url() -> str:
    if url := os.environ.get("REACT_APP_BACKEND_URL"):
        return url
    with open("/app/frontend/.env") as env_file:
        content = env_file.read()
    return content.split("REACT_APP_BACKEND_URL=")[1].split("\n")[0].strip()


BASE_URL = _get_base_url()
BASE_URL = BASE_URL.rstrip("/")


@pytest.fixture(scope="module")
def admin_session():
    """Session with admin httpOnly cookies set"""
    session = requests.Session()
    resp = session.post(f"{BASE_URL}/api/auth/token/", json={"email": "admin@blog.com", "password": "admin123"})
    if resp.status_code == 200:
        return session
    pytest.skip(f"Admin login failed: {resp.status_code} {resp.text}")


# Keep for backward compat
@pytest.fixture(scope="module")
def admin_token(admin_session):
    return "cookie-based"


@pytest.fixture(scope="module")
def admin_headers(admin_session):
    return admin_session


# ---- Auth tests ----


def test_admin_login():
    resp = requests.post(f"{BASE_URL}/api/auth/token/", json={"email": "admin@blog.com", "password": "admin123"})
    assert resp.status_code == 200
    data = resp.json()
    assert "user" in data
    assert data["user"]["email"] == "admin@blog.com"


def test_register_new_user():
    resp = requests.post(
        f"{BASE_URL}/api/auth/register/",
        json={
            "email": "testuser@blog.com",
            "username": "testuser",
            "password": "test123456",
            "password2": "test123456",
        },
    )
    # 201 or 400 if already exists
    assert resp.status_code in [200, 201, 400], f"Unexpected: {resp.status_code} {resp.text}"


def test_login_testuser():
    resp = requests.post(f"{BASE_URL}/api/auth/token/", json={"email": "testuser@blog.com", "password": "test123456"})
    assert resp.status_code == 200


def test_me_endpoint(admin_session):
    resp = admin_session.get(f"{BASE_URL}/api/auth/me/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "admin@blog.com"


def test_invalid_login():
    resp = requests.post(f"{BASE_URL}/api/auth/token/", json={"email": "bad@bad.com", "password": "wrongpass"})
    assert resp.status_code in [400, 401]


# ---- Posts tests ----


def test_list_posts():
    resp = requests.get(f"{BASE_URL}/api/posts/")
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data
    assert data["count"] >= 3


def test_get_post_detail():
    resp = requests.get(f"{BASE_URL}/api/posts/how-ai-is-transforming-content-creation/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "How AI is Transforming Content Creation"
    assert "ai_summary" in data


def test_create_post(admin_session):
    resp = admin_session.post(
        f"{BASE_URL}/api/posts/",
        json={
            "title": "TEST_Blog Post Automation",
            "content": "This is a test post created by automation.",
            "status": "published",
        },
    )
    assert resp.status_code == 201, f"{resp.status_code} {resp.text}"
    data = resp.json()
    assert "slug" in data
    return data["slug"]


def test_create_and_update_post(admin_session):
    # Create
    resp = admin_session.post(
        f"{BASE_URL}/api/posts/", json={"title": "TEST_Update Post", "content": "Original content.", "status": "draft"}
    )
    assert resp.status_code == 201
    slug = resp.json()["slug"]

    # Update (PATCH not PUT)
    upd = admin_session.patch(
        f"{BASE_URL}/api/posts/{slug}/",
        json={"title": "TEST_Update Post", "content": "Updated content.", "status": "published"},
    )
    assert upd.status_code == 200
    assert upd.json()["content"] == "Updated content."

    # Delete
    del_resp = admin_session.delete(f"{BASE_URL}/api/posts/{slug}/")
    assert del_resp.status_code == 204


# ---- Categories ----


def test_list_categories():
    resp = requests.get(f"{BASE_URL}/api/categories/")
    assert resp.status_code == 200
    data = resp.json()
    # paginated or list
    items = data.get("results", data) if isinstance(data, dict) else data
    assert len(items) >= 3


# ---- Tags ----


def test_list_tags():
    resp = requests.get(f"{BASE_URL}/api/tags/")
    assert resp.status_code == 200


# ---- Comments ----


def test_create_and_delete_comment(admin_session):
    slug = "how-ai-is-transforming-content-creation"
    resp = admin_session.post(f"{BASE_URL}/api/posts/{slug}/comments/", json={"content": "TEST_ Great post!"})
    assert resp.status_code == 201, f"{resp.status_code} {resp.text}"
    comment_id = resp.json()["id"]

    # Delete comment
    del_resp = admin_session.delete(f"{BASE_URL}/api/comments/{comment_id}/")
    assert del_resp.status_code in [200, 204], f"{del_resp.status_code} {del_resp.text}"


# ---- Admin users list ----


def test_admin_users_list(admin_session):
    resp = admin_session.get(f"{BASE_URL}/api/auth/users/")
    assert resp.status_code == 200


# ---- Search ----


def test_search_posts():
    resp = requests.get(f"{BASE_URL}/api/posts/?search=AI")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 1


# ---- My posts ----


def test_my_posts(admin_session):
    resp = admin_session.get(f"{BASE_URL}/api/posts/my/")
    assert resp.status_code == 200
