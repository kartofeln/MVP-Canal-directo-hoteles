from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.default_mice_targets import DEFAULT_MICE_BATCH
from app.models import IngestionRun, KeywordSnapshot
from app.services.dataforseo import fetch_market_batch
from app.config import Settings


def _as_float(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def run_ingestion(
    db: Session,
    settings: Settings,
    markets: list[dict[str, Any]] | None,
) -> UUID:
    batch = markets or DEFAULT_MICE_BATCH
    run = IngestionRun(status="running", meta={"markets": len(batch)})
    db.add(run)
    db.commit()
    db.refresh(run)
    run_id = run.id

    try:
        saved = 0
        api_notes: list[str] = []
        for m in batch:
            label = m["label"]
            loc = m["location_code"]
            lang = m["language_code"]
            kws = m["keywords"]
            rows, raw = fetch_market_batch(settings, loc, lang, kws)
            if not rows:
                sc = raw.get("status_code")
                sm = raw.get("status_message") or raw.get("message")
                terr = raw.get("task_errors")
                if terr:
                    api_notes.append(f"{label}: " + "; ".join(terr)[:500])
                elif raw.get("http_status"):
                    api_notes.append(
                        f"{label}: HTTP {raw.get('http_status')} {raw.get('body_preview', '')[:200]!r}"
                    )
                else:
                    api_notes.append(
                        f"{label}: status_code={sc!r} message={sm!r}"
                        if sm or sc is not None
                        else f"{label}: sin filas (credenciales, saldo o límites DataForSEO)"
                    )
            for row in rows:
                vol = row.get("search_volume")
                if vol is not None and not isinstance(vol, int):
                    try:
                        vol = int(vol)
                    except (TypeError, ValueError):
                        vol = None
                snap = KeywordSnapshot(
                    run_id=run_id,
                    market_label=label,
                    location_code=loc,
                    language_code=lang,
                    keyword=row.get("keyword") or "",
                    search_volume=vol,
                    competition=_as_float(row.get("competition")),
                    cpc=_as_float(row.get("cpc")),
                    raw_item=row.get("raw"),
                )
                db.add(snap)
                saved += 1
        if saved == 0:
            run.status = "error"
            run.error_message = "Ninguna keyword guardada. " + " | ".join(api_notes)[:3900]
        else:
            run.status = "ok"
            run.error_message = None
    except Exception as e:
        run.status = "error"
        run.error_message = str(e)[:4000]
    finally:
        run.finished_at = datetime.now(timezone.utc)
        db.commit()

    return run_id


def seed_demo_snapshots(db: Session) -> UUID:
    """
    Inserta un run OK con filas ficticias (misma forma que una ingesta real).
    No llama a DataForSEO. Solo para probar /latest, /csv y Excel.
    """
    run = IngestionRun(status="ok", meta={"source": "demo_local"}, error_message=None)
    db.add(run)
    db.commit()
    db.refresh(run)
    run_id = run.id
    n = 0
    for m in DEFAULT_MICE_BATCH:
        for kw in m["keywords"]:
            n += 1
            snap = KeywordSnapshot(
                run_id=run_id,
                market_label=m["label"],
                location_code=m["location_code"],
                language_code=m["language_code"],
                keyword=kw,
                search_volume=800 + (n * 111) % 9000,
                competition=0.4 + (n % 8) * 0.07,
                cpc=0.5 + (n % 10) * 0.15,
                raw_item={"demo": True},
            )
            db.add(snap)
    run.finished_at = datetime.now(timezone.utc)
    db.commit()
    return run_id


def get_latest_ok_run(db: Session) -> IngestionRun | None:
    """Último run OK que tenga al menos un snapshot (evita runs vacíos antiguos)."""
    runs = db.execute(
        select(IngestionRun)
        .where(IngestionRun.status == "ok")
        .order_by(desc(IngestionRun.started_at))
        .limit(30)
    ).scalars().all()
    for run in runs:
        n = db.scalar(
            select(func.count())
            .select_from(KeywordSnapshot)
            .where(KeywordSnapshot.run_id == run.id)
        )
        if n and n > 0:
            return run
    return None


def snapshots_to_markdown(db: Session, run_id: UUID) -> tuple[str, datetime]:
    run = db.get(IngestionRun, run_id)
    if not run:
        raise ValueError("run_id no encontrado")
    q = select(KeywordSnapshot).where(KeywordSnapshot.run_id == run_id)
    rows = db.execute(q).scalars().all()
    lines = ["| Mercado | Keyword | Volumen | Competencia | CPC |", "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: (-(x.search_volume or 0), x.market_label, x.keyword)):
        vol = r.search_volume if r.search_volume is not None else "—"
        comp = r.competition if r.competition is not None else "—"
        cpc = r.cpc if r.cpc is not None else "—"
        lines.append(f"| {r.market_label} | {r.keyword} | {vol} | {comp} | {cpc} |")
    as_of = run.finished_at or run.started_at
    return "\n".join(lines), as_of
