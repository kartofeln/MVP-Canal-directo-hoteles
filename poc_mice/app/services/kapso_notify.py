import httpx

from app.config import Settings

# Documentación: https://docs.kapso.ai/ — ajusta path si tu cuenta usa otra versión.
KAPSO_API_BASE = "https://api.kapso.ai/meta/whatsapp/v24.0"


def send_text_message(settings: Settings, to_e164: str, body: str) -> dict:
    """
    Envío mínimo de texto. Requiere número conectado en Kapso y API key.
    El payload exacto puede variar según plantillas Meta; este es un esqueleto POC.
    """
    if not settings.kapso_api_key:
        raise ValueError("Falta KAPSO_API_KEY")
    if not to_e164:
        raise ValueError("Falta número destino (KAPSO_TEST_TO)")

    headers = {
        "X-API-Key": settings.kapso_api_key,
        "Content-Type": "application/json",
    }
    # Nota: en producción suele usarse message template o el endpoint oficial de tu app en Kapso.
    payload = {
        "messaging_product": "whatsapp",
        "to": to_e164,
        "type": "text",
        "text": {"body": body[:4096]},
    }
    with httpx.Client(timeout=60.0) as client:
        r = client.post(
            f"{KAPSO_API_BASE}/messages",
            headers=headers,
            json=payload,
        )
    try:
        return {"status_code": r.status_code, "body": r.json()}
    except Exception:
        return {"status_code": r.status_code, "body": r.text}
