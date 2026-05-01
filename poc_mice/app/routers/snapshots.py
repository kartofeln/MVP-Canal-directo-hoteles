from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import IngestionRun, KeywordSnapshot
from app.services.snapshot_export import snapshots_to_csv_bytes, snapshots_to_markdown
from app.services.snapshot_queries import (
    csv_filename_for_run,
    md_filename_for_run,
    require_latest_snapshots,
)

router = APIRouter(prefix="/v1/snapshots", tags=["snapshots"])


@router.get(
    "/latest",
    summary="Último snapshot (JSON, o query download=csv|md)",
)
def latest(
    db: Session = Depends(get_db),
    download: str | None = Query(
        default=None,
        description='Descarga: escribe "csv" o "md". Vacío = respuesta JSON.',
    ),
):
    run, rows = require_latest_snapshots(db)
    if download:
        kind = download.strip().lower()
        if kind == "csv":
            body = snapshots_to_csv_bytes(run, rows)
            name = csv_filename_for_run(run.id)
            return Response(
                content=body,
                media_type="text/csv; charset=utf-8",
                headers={"Content-Disposition": f'attachment; filename="{name}"'},
            )
        if kind in ("md", "markdown"):
            text = snapshots_to_markdown(run, rows)
            name = md_filename_for_run(run.id)
            return Response(
                content=text.encode("utf-8"),
                media_type="text/markdown; charset=utf-8",
                headers={"Content-Disposition": f'attachment; filename="{name}"'},
            )
        raise HTTPException(
            status_code=400,
            detail='Parámetro download: usa "csv" o "md" (o déjalo vacío para JSON).',
        )
    return {
        "run_id": str(run.id),
        "started_at": run.started_at,
        "finished_at": run.finished_at,
        "rows": [
            {
                "market": r.market_label,
                "location_code": r.location_code,
                "language_code": r.language_code,
                "keyword": r.keyword,
                "search_volume": r.search_volume,
                "competition": r.competition,
                "cpc": r.cpc,
            }
            for r in rows
        ],
    }


@router.get("/latest/csv", summary="Descargar CSV (LinkedIn / Excel)")
def latest_csv_alias(db: Session = Depends(get_db)):
    run, rows = require_latest_snapshots(db)
    body = snapshots_to_csv_bytes(run, rows)
    name = csv_filename_for_run(run.id)
    return Response(
        content=body,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


@router.get("/latest/md", summary="Descargar Markdown")
def latest_md_alias(db: Session = Depends(get_db)):
    run, rows = require_latest_snapshots(db)
    text = snapshots_to_markdown(run, rows)
    name = md_filename_for_run(run.id)
    return Response(
        content=text.encode("utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


def _by_run_rows_or_404(db: Session, run_id: UUID) -> tuple[IngestionRun, list[KeywordSnapshot]]:
    run = db.get(IngestionRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run no encontrado")
    if run.status != "ok":
        raise HTTPException(status_code=400, detail="El run no está en estado ok")
    rows = list(
        db.execute(
            select(KeywordSnapshot).where(KeywordSnapshot.run_id == run_id)
        ).scalars().all()
    )
    return run, rows


# Rutas más específicas antes que /by-run/{run_id}
@router.get("/by-run/{run_id}/csv")
def by_run_csv(run_id: UUID, db: Session = Depends(get_db)):
    run, rows = _by_run_rows_or_404(db, run_id)
    body = snapshots_to_csv_bytes(run, rows)
    name = csv_filename_for_run(run.id)
    return Response(
        content=body,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


@router.get("/by-run/{run_id}/md")
def by_run_md(run_id: UUID, db: Session = Depends(get_db)):
    run, rows = _by_run_rows_or_404(db, run_id)
    text = snapshots_to_markdown(run, rows)
    name = md_filename_for_run(run.id)
    return Response(
        content=text.encode("utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


@router.get("/by-run/{run_id}/export.csv")
def export_by_run_csv(run_id: UUID, db: Session = Depends(get_db)):
    run, rows = _by_run_rows_or_404(db, run_id)
    body = snapshots_to_csv_bytes(run, rows)
    name = csv_filename_for_run(run.id)
    return Response(
        content=body,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


@router.get("/by-run/{run_id}/export.md")
def export_by_run_md(run_id: UUID, db: Session = Depends(get_db)):
    run, rows = _by_run_rows_or_404(db, run_id)
    text = snapshots_to_markdown(run, rows)
    name = md_filename_for_run(run.id)
    return Response(
        content=text.encode("utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


@router.get("/by-run/{run_id}")
def by_run(run_id: UUID, db: Session = Depends(get_db)):
    run = db.get(IngestionRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run no encontrado")
    rows = db.execute(
        select(KeywordSnapshot).where(KeywordSnapshot.run_id == run_id)
    ).scalars().all()
    return {
        "run_id": str(run.id),
        "status": run.status,
        "rows": [
            {
                "market": r.market_label,
                "keyword": r.keyword,
                "search_volume": r.search_volume,
                "competition": r.competition,
                "cpc": r.cpc,
            }
            for r in rows
        ],
    }
