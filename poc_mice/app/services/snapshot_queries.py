"""Consultas para exportar snapshots (último run con filas)."""

from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models import IngestionRun, KeywordSnapshot
from app.services.ingestion import get_latest_ok_run

_MSG_VACIO = (
    "No hay filas guardadas para exportar. "
    "Ejecuta POST /v1/ingest/run con DataForSEO bien configurado. "
    "Si el run falla, abre GET /v1/ingest/runs/{run_id} y lee error_message. "
    "Sin datos en la base de datos no se puede generar un CSV."
)


def dashboard_empty_hints(db: Session) -> dict:
    """Contexto para /dashboard cuando no hay último run OK con filas."""
    last = db.execute(
        select(IngestionRun).order_by(desc(IngestionRun.started_at)).limit(1)
    ).scalars().first()
    if not last:
        return {
            "last_run_id_short": None,
            "last_run_status": None,
            "last_run_snapshots": 0,
            "last_run_error": None,
        }
    n = db.scalar(
        select(func.count())
        .select_from(KeywordSnapshot)
        .where(KeywordSnapshot.run_id == last.id)
    )
    err = (last.error_message or "").strip()
    return {
        "last_run_id_short": str(last.id)[:8],
        "last_run_status": last.status,
        "last_run_snapshots": int(n or 0),
        "last_run_error": (err[:500] + "…") if len(err) > 500 else err or None,
    }


def require_latest_snapshots(db: Session) -> tuple[IngestionRun, list[KeywordSnapshot]]:
    run = get_latest_ok_run(db)
    if not run:
        raise HTTPException(status_code=404, detail=_MSG_VACIO)
    rows = list(
        db.execute(
            select(KeywordSnapshot).where(KeywordSnapshot.run_id == run.id)
        ).scalars().all()
    )
    return run, rows


def export_basename(run_id: UUID) -> str:
    return f"mice_keywords_{str(run_id)[:8]}"


def csv_filename_for_run(run_id: UUID) -> str:
    return f"{export_basename(run_id)}.csv"


def md_filename_for_run(run_id: UUID) -> str:
    return f"{export_basename(run_id)}.md"
