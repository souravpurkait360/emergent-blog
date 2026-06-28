"""Root conftest — shared fixtures available to all apps' test suites."""

import os

import pytest
import requests


def _get_base_url() -> str:
    if url := os.environ.get("REACT_APP_BACKEND_URL"):
        return url
    with open("/app/frontend/.env") as env_file:
        content = env_file.read()
    return content.split("REACT_APP_BACKEND_URL=")[1].split("\n")[0].strip()


BASE_URL = _get_base_url().rstrip("/")


@pytest.fixture(scope="module")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="module")
def admin_session() -> requests.Session:
    """Authenticated requests.Session with admin httpOnly cookies."""
    session = requests.Session()
    resp = session.post(
        f"{BASE_URL}/api/auth/token/",
        json={"email": "admin@blog.com", "password": "admin123"},
    )
    if resp.status_code != 200:
        pytest.skip(f"Admin login failed: {resp.status_code} {resp.text}")
    return session
