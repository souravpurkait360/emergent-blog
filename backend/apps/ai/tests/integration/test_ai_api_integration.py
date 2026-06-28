"""Integration tests — AI API (ai app).

Covers: /api/ai/summarize/ and /api/ai/assist/.
Uses a live HTTP session against the running backend.
"""

from conftest import BASE_URL
import requests

SAMPLE_SLUG = "how-ai-is-transforming-content-creation"


def test_summarize_requires_auth() -> None:
    resp = requests.post(
        f"{BASE_URL}/api/ai/summarize/",
        json={"post_slug": SAMPLE_SLUG},
    )
    assert resp.status_code == 401


def test_assist_requires_auth() -> None:
    resp = requests.post(
        f"{BASE_URL}/api/ai/assist/",
        json={"content": "AI is changing the world"},
    )
    assert resp.status_code == 401


def test_summarize_authenticated(admin_session) -> None:
    resp = admin_session.post(
        f"{BASE_URL}/api/ai/summarize/",
        json={"post_slug": SAMPLE_SLUG},
    )
    # 200 with summary or 402/503 if LLM key quota is exhausted — both valid
    assert resp.status_code in (200, 402, 503), f"{resp.status_code} {resp.text}"
    if resp.status_code == 200:
        assert "summary" in resp.json()


def test_assist_authenticated(admin_session) -> None:
    resp = admin_session.post(
        f"{BASE_URL}/api/ai/assist/",
        json={"content": "Artificial intelligence is changing the world of"},
    )
    assert resp.status_code in (200, 402, 503), f"{resp.status_code} {resp.text}"
    if resp.status_code == 200:
        # endpoint returns {"suggestion": "..."} per AIAssistAPIView
        data = resp.json()
        assert any(k in data for k in ("suggestion", "continuation", "result")), f"Unexpected keys: {data.keys()}"
