from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import uuid

from app.db import get_db
from app.models import Hotel, CheckRun, Finding
from app.services.web_audit import audit_website

router = APIRouter(prefix="/v1/canal-directo", tags=["canal_directo"])


# -----------------------------
# CREAR HOTEL
# -----------------------------
@router.post("/hotels")
def create_hotel(payload: dict, db: Session = Depends(get_db)):
    hotel = Hotel(
        id=str(uuid.uuid4()),
        name=payload.get("name"),
        city=payload.get("city"),
        country_code=payload.get("country_code"),
        official_domain=payload.get("official_domain"),
        brand_query=payload.get("brand_query"),
        active=True,
    )
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    return hotel


# -----------------------------
# LISTAR HOTELES
# -----------------------------
@router.get("/hotels")
def list_hotels(db: Session = Depends(get_db)):
    return db.query(Hotel).all()


# -----------------------------
# EJECUTAR CHECK
# -----------------------------
@router.post("/checks/run")
def run_check(hotel_id: str = Query(...), db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()

    if not hotel:
        return {"error": "Hotel no encontrado"}

    audit = audit_website(hotel.official_domain)

    run = CheckRun(
        id=str(uuid.uuid4()),
        hotel_id=hotel.id,
        status=audit["status"],
        score=audit["score"],
    )

    db.add(run)
    db.flush()

    for f in audit["findings"]:
        finding = Finding(
            id=str(uuid.uuid4()),
            run_id=run.id,
            severity=f["severity"],
            message=f["message"],
        )
        db.add(finding)

    db.commit()
    db.refresh(run)

    return {"ok": True, "run_id": run.id}


# -----------------------------
# SUMMARY PARA REPORT
# -----------------------------
def summary(db: Session):
    hotels = db.query(Hotel).all()

    result = []

    for h in hotels:
        run = (
            db.query(CheckRun)
            .filter(CheckRun.hotel_id == h.id)
            .order_by(CheckRun.id.desc())
            .first()
        )

        if run:
            findings = (
                db.query(Finding)
                .filter(Finding.run_id == run.id)
                .all()
            )
            run.findings = findings

        result.append({
            "hotel": h,
            "latest_run": run
        })

    return result
