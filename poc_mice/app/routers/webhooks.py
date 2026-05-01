from fastapi import APIRouter, Depends, Header, HTTPException, Request

from app.config import Settings, get_settings

router = APIRouter(tags=["webhooks"])


@router.post("/webhooks/kapso")
async def kapso_webhook(
    request: Request,
    settings: Settings = Depends(get_settings),
    x_webhook_secret: str | None = Header(default=None, alias="X-Webhook-Secret"),
):
    """
    Recibe eventos de Kapso (mensajes entrantes, estado de entrega, etc.).
    Si KAPSO_WEBHOOK_SECRET está definido, valida el header X-Webhook-Secret.
    Amplía aquí: parsear texto del usuario, llamar a brief/generate, responder vía API Kapso.
    """
    if settings.kapso_webhook_secret:
        if x_webhook_secret != settings.kapso_webhook_secret:
            raise HTTPException(status_code=401, detail="Invalid webhook secret")

    payload = await request.json()
    # POC: eco + ACK. Sustituye por lógica conversacional.
    return {
        "ok": True,
        "echo_keys": list(payload.keys()) if isinstance(payload, dict) else [],
        "hint": "Conecta este URL en el panel de Kapso y añade lógica en app/routers/webhooks.py",
    }
