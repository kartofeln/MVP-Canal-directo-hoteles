from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import get_db
from app.models import IngestionRun, KeywordSnapshot
from app.schemas import IngestRunBody, IngestRunResponse
from app.services.ingestion import run_ingestion, seed_demo_snapshots

router = APIRouter(prefix="/v1/ingest", tags=["ingest"])


@router.post("/run", response_model=IngestRunResponse)
def post_run(
    body: IngestRunBody | None = None,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    markets = None
    if body and body.markets:
        markets = [m.model_dump() for m in body.markets]
    try:
        run_id = run_ingestion(db, settings, markets)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    run = db.get(IngestionRun, run_id)
    return IngestRunResponse(
        run_id=run_id,
        status=run.status if run else "unknown",
        message="Ingesta finalizada" if run and run.status == "ok" else (run.error_message or "Error"),
    )


@router.post("/demo-local", response_model=IngestRunResponse)
def post_demo_local(
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """
    Rellena la base con datos **ficticios** (no DataForSEO).
    Activa `POC_ALLOW_FAKE_DATA=1` en `.env` y reinicia uvicorn.
    Sirve para probar `/v1/snapshots/latest`, `/csv` y Excel/LinkedIn con flujo completo.
    """
    if not settings.poc_allow_fake_data:
        raise HTTPException(
            status_code=403,
            detail=(
                "Pon POC_ALLOW_FAKE_DATA=1 en poc_mice/.env y reinicia uvicorn. "
                "Los números serán de demostración, no para publicar como datos de mercado reales."
            ),
        )
    run_id = seed_demo_snapshots(db)
    return IngestRunResponse(
        run_id=run_id,
        status="ok",
        message="Demo local: filas ficticias insertadas. Abre GET /v1/snapshots/latest o http://127.0.0.1:8000/csv",
    )


@router.get("/runs/{run_id}")
def get_run(run_id: UUID, db: Session = Depends(get_db)):
    run = db.get(IngestionRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run no encontrado")
    n = db.scalar(
        select(func.count()).select_from(KeywordSnapshot).where(KeywordSnapshot.run_id == run_id)
    )
    return {
        "id": str(run.id),
        "status": run.status,
        "started_at": run.started_at,
        "finished_at": run.finished_at,
        "error_message": run.error_message,
        "snapshots": n,
    }
