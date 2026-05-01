"""Vista HTML bonita (sin Excel)."""

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.services.snapshot_queries import dashboard_empty_hints, require_latest_snapshots

router = APIRouter(tags=["ui"])

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))


def _fmt(v):
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


@router.get("/dashboard", response_class=HTMLResponse, summary="Vista bonita: tabla + gráfico")
def mice_dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        run, snaps = require_latest_snapshots(db)
    except HTTPException:
        settings = get_settings()
        return templates.TemplateResponse(
            request,
            "mice_dashboard.html",
            {
                "has_data": False,
                "hints": dashboard_empty_hints(db),
                "demo_enabled": bool(settings.poc_allow_fake_data),
            },
        )

    rows_sorted = sorted(
        snaps,
        key=lambda x: (-(x.search_volume or 0), x.market_label, x.keyword),
    )
    rows = [
        {
            "market": s.market_label,
            "keyword": s.keyword,
            "volume": s.search_volume if s.search_volume is not None else "—",
            "competition": _fmt(s.competition),
            "cpc": _fmt(s.cpc),
        }
        for s in rows_sorted
    ]

    top = rows_sorted[:14]
    chart_labels = [f"{s.market_label[:3]} · {s.keyword[:28]}{'…' if len(s.keyword) > 28 else ''}" for s in top]
    chart_values = [s.search_volume or 0 for s in top]

    fin = run.finished_at.isoformat() if run.finished_at else "—"

    return templates.TemplateResponse(
        request,
        "mice_dashboard.html",
        {
            "has_data": True,
            "finished_at": fin,
            "run_id_short": str(run.id)[:8],
            "rows": rows,
            "chart_labels": chart_labels,
            "chart_values": chart_values,
        },
    )
