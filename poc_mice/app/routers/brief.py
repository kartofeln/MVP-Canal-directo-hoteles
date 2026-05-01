from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import get_db
from app.models import IngestionRun
from app.schemas import BriefRequest, BriefResponse
from app.services.ingestion import get_latest_ok_run, snapshots_to_markdown
from app.services.anthropic_brief import build_brief_from_table
from app.services.kapso_notify import send_text_message

router = APIRouter(prefix="/v1/brief", tags=["brief"])


@router.post("/generate", response_model=BriefResponse)
def generate_brief(
    body: BriefRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    run_id = body.run_id
    if run_id is None:
        run = get_latest_ok_run(db)
        if not run:
            raise HTTPException(status_code=404, detail="No hay ingestas OK.")
        run_id = run.id
    else:
        run = db.get(IngestionRun, run_id)
        if not run or run.status != "ok":
            raise HTTPException(status_code=400, detail="Run inexistente o no OK.")

    try:
        md, as_of = snapshots_to_markdown(db, run_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    try:
        brief = build_brief_from_table(settings, md, as_of.isoformat())
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e

    whatsapp_sent = False
    whatsapp_detail = None
    if body.send_whatsapp:
        try:
            whatsapp_detail = send_text_message(
                settings,
                settings.kapso_test_to,
                f"POC MICE — {as_of.date()}\n\n{brief[:3500]}",
            )
            whatsapp_sent = whatsapp_detail.get("status_code") in (200, 201)
        except ValueError as e:
            whatsapp_detail = {"error": str(e)}

    return BriefResponse(
        run_id=run_id,
        data_as_of=as_of,
        brief_text=brief,
        whatsapp_sent=whatsapp_sent,
        whatsapp_detail=whatsapp_detail,
    )
