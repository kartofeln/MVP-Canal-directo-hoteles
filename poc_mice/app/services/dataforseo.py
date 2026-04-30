import base64
from typing import Any

import httpx

from app.config import Settings


DATAFORSEO_SEARCH_VOLUME_URL = (
    "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
)


def _headers(settings: Settings) -> dict[str, str]:
    raw = f"{settings.dataforseo_login}:{settings.dataforseo_password}".encode()
    token = base64.b64encode(raw).decode()
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }


def fetch_market_batch(
    settings: Settings,
    location_code: int,
    language_code: str,
    keywords: list[str],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Una llamada DataForSEO por mercado (mismo location + language + lista keywords).
    Devuelve (filas normalizadas, respuesta cruda mínima para depuración).
    """
    if not settings.dataforseo_login or not settings.dataforseo_password:
        raise ValueError("Faltan DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD")

    payload = [
        {
            "location_code": location_code,
            "language_code": language_code,
            "keywords": keywords,
        }
    ]
    with httpx.Client(timeout=120.0) as client:
        r = client.post(
            DATAFORSEO_SEARCH_VOLUME_URL,
            headers=_headers(settings),
            json=payload,
        )
    try:
        data = r.json()
    except Exception:
        return [], {"http_status": r.status_code, "body_preview": (r.text or "")[:500]}

    rows: list[dict[str, Any]] = []
    task_errors: list[str] = []

    if data.get("status_code") != 20000:
        return rows, data

    for task in data.get("tasks") or []:
        tsc = task.get("status_code")
        if tsc != 20000:
            task_errors.append(
                f"task status_code={tsc!r} message={task.get('status_message')!r}"
            )
            continue
        for item in task.get("result") or []:
            rows.append(
                {
                    "keyword": item.get("keyword"),
                    "search_volume": item.get("search_volume"),
                    "competition": item.get("competition"),
                    "cpc": item.get("cpc"),
                    "raw": item,
                }
            )

    meta: dict[str, Any] = {
        "status_code": data.get("status_code"),
        "tasks_count": len(data.get("tasks") or []),
    }
    if task_errors:
        meta["task_errors"] = task_errors
    return rows, meta
