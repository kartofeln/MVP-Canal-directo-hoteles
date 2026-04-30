from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.routers import brief, ingest, mice_ui, snapshots, webhooks
from app.services.snapshot_export import snapshots_to_csv_bytes
from app.services.snapshot_queries import csv_filename_for_run, require_latest_snapshots

# Sube este valor cuando cambies el POC; debe coincidir con GET /meta-poc
POC_BUILD = "2026-03-29f"


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("\n" + "=" * 60)
    print(f"  POC MICE  build={POC_BUILD}")
    print("  Comprueba en el navegador: /meta-poc en el MISMO puerto que muestra uvicorn arriba")
    print("  Si /meta-poc da 404, NO es este código (otro proceso en ese puerto).")
    print("=" * 60 + "\n")
    yield


app = FastAPI(
    title="POC MICE — DataForSEO + Postgres + Claude + Kapso",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(ingest.router)
app.include_router(snapshots.router)
app.include_router(brief.router)
app.include_router(webhooks.router)
app.include_router(mice_ui.router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/meta-poc", tags=["ayuda"])
def meta_poc():
    """
    Si esta ruta da 404, estás ejecutando **otro** proyecto o una copia vieja del código.
    Deberías ver `build` = POC_BUILD del repo actual y rutas que faltan en tu openapi.json.
    """
    return {
        "build": POC_BUILD,
        "debe_existir_en_openapi": [
            "/meta-poc",
            "/csv",
            "/dashboard",
            "/guia",
            "/health",
            "/v1/ingest/demo-local",
            "/v1/snapshots/latest/csv",
        ],
        "arreglo_tipico": (
            "Para el servidor (Ctrl+C). cd a poc_mice. "
            "PYTHONPATH=poc_mice y: uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
        ),
    }


@app.get(
    "/csv",
    tags=["descarga"],
    summary="👉 Atajo: descargar último CSV (misma lógica que /v1/snapshots/latest/csv)",
)
def descargar_csv_atajo(db: Session = Depends(get_db)):
    run, rows = require_latest_snapshots(db)
    body = snapshots_to_csv_bytes(run, rows)
    name = csv_filename_for_run(run.id)
    return Response(
        content=body,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


def _payload_guia_rutas() -> dict:
    # El puerto real lo pones tú en uvicorn (--port); 8010 es el default de run_api.ps1
    import os

    p = os.environ.get("POC_PORT", "8010")
    base = f"http://127.0.0.1:{p}"
    return {
        "docs_swagger": f"{base}/docs",
        "ultimo_json": f"{base}/v1/snapshots/latest",
        "ultimo_csv_largo": f"{base}/v1/snapshots/latest/csv",
        "ultimo_csv_corto": f"{base}/csv",
        "ingesta_real": "POST " + f"{base}/v1/ingest/run" + " cuerpo {}",
        "ingesta_demo": "POST " + f"{base}/v1/ingest/demo-local" + " (POC_ALLOW_FAKE_DATA=1 en .env)",
        "nota": "Todas las rutas API llevan prefijo /v1/ excepto /docs /health /csv",
    }


@app.get("/health")
def health(
    rutas: bool = Query(
        default=False,
        description="Si es true, incluye las URLs útiles del POC en la respuesta.",
    ),
):
    out: dict = {"status": "ok", "app": "poc_mice"}
    if rutas:
        out["guia"] = _payload_guia_rutas()
    return out


@app.get("/guia-rutas", tags=["ayuda"], operation_id="guia_rutas_hyphen")
def guia_rutas_hyphen():
    return _payload_guia_rutas()


@app.get("/guia", tags=["ayuda"], operation_id="guia_rutas_short")
def guia_rutas_short():
    return _payload_guia_rutas()


@app.get("/ayuda-rutas", tags=["ayuda"], operation_id="guia_rutas_ayuda")
def guia_rutas_ayuda():
    return _payload_guia_rutas()
