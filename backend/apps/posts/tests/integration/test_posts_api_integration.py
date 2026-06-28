"""Integration tests — Posts API (posts app).

Covers: list, detail, create, update, delete, categories, tags,
        comments, search, my-posts.
Uses a live HTTP session against the running backend.
"""

from conftest import BASE_URL
import requests

SAMPLE_SLUG = "how-ai-is-transforming-content-creation"


# ---------------------------------------------------------------------------
# Post list
# ---------------------------------------------------------------------------


def test_list_posts_returns_paginated_results() -> None:
    resp = requests.get(f"{BASE_URL}/api/posts/")
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data
    assert "count" in data
    assert data["count"] >= 1


def test_list_posts_unauthenticated_allowed() -> None:
    resp = requests.get(f"{BASE_URL}/api/posts/")
    assert resp.status_code == 200


def test_search_filters_posts_by_keyword() -> None:
    resp = requests.get(f"{BASE_URL}/api/posts/?search=AI")
    assert resp.status_code == 200
    assert resp.json()["count"] >= 1


# ---------------------------------------------------------------------------
# Post detail
# ---------------------------------------------------------------------------


def test_get_post_detail_by_slug() -> None:
    resp = requests.get(f"{BASE_URL}/api/posts/{SAMPLE_SLUG}/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "How AI is Transforming Content Creation"
    assert "content" in data
    assert "ai_summary" in data
    assert "comments" in data


def test_get_nonexistent_post_returns_404() -> None:
    resp = requests.get(f"{BASE_URL}/api/posts/does-not-exist-xyz/")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Post create / update / delete
# ---------------------------------------------------------------------------


def test_create_post_requires_auth() -> None:
    resp = requests.post(
        f"{BASE_URL}/api/posts/",
        json={"title": "Anon post", "content": "Should fail."},
    )
    assert resp.status_code == 401


def test_authenticated_user_can_create_post(admin_session) -> None:
    resp = admin_session.post(
        f"{BASE_URL}/api/posts/",
        json={"title": "TEST_Integration Post", "content": "Body.", "status": "published"},
    )
    assert resp.status_code == 201, f"{resp.status_code} {resp.text}"
    assert "slug" in resp.json()


def test_create_update_delete_post_lifecycle(admin_session) -> None:
    # Create
    create = admin_session.post(
        f"{BASE_URL}/api/posts/",
        json={"title": "TEST_Lifecycle Post", "content": "Original.", "status": "draft"},
    )
    assert create.status_code == 201
    slug = create.json()["slug"]

    # Update (PATCH)
    patch = admin_session.patch(
        f"{BASE_URL}/api/posts/{slug}/",
        json={"content": "Updated content.", "status": "published"},
    )
    assert patch.status_code == 200
    assert patch.json()["content"] == "Updated content."

    # Delete
    delete = admin_session.delete(f"{BASE_URL}/api/posts/{slug}/")
    assert delete.status_code == 204

    # Confirm gone
    assert requests.get(f"{BASE_URL}/api/posts/{slug}/").status_code == 404


# ---------------------------------------------------------------------------
# My posts
# ---------------------------------------------------------------------------


def test_my_posts_requires_auth() -> None:
    resp = requests.get(f"{BASE_URL}/api/posts/my/")
    assert resp.status_code == 401


def test_my_posts_returns_own_posts(admin_session) -> None:
    resp = admin_session.get(f"{BASE_URL}/api/posts/my/")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Categories & Tags
# ---------------------------------------------------------------------------


def test_list_categories_returns_results() -> None:
    resp = requests.get(f"{BASE_URL}/api/categories/")
    assert resp.status_code == 200
    items = resp.json() if isinstance(resp.json(), list) else resp.json().get("results", [])
    assert len(items) >= 1


def test_list_tags_returns_200() -> None:
    resp = requests.get(f"{BASE_URL}/api/tags/")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Comments
# ---------------------------------------------------------------------------


def test_create_and_delete_comment(admin_session) -> None:
    create = admin_session.post(
        f"{BASE_URL}/api/posts/{SAMPLE_SLUG}/comments/",
        json={"content": "TEST_ Integration comment."},
    )
    assert create.status_code == 201, f"{create.status_code} {create.text}"
    comment_id = create.json()["id"]

    delete = admin_session.delete(f"{BASE_URL}/api/comments/{comment_id}/")
    assert delete.status_code in (200, 204), f"{delete.status_code} {delete.text}"


def test_create_comment_requires_auth() -> None:
    resp = requests.post(
        f"{BASE_URL}/api/posts/{SAMPLE_SLUG}/comments/",
        json={"content": "Anon comment — should fail."},
    )
    assert resp.status_code == 401
