from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class MarketInput(BaseModel):
    label: str
    location_code: int
    language_code: str
    keywords: list[str] = Field(min_length=1)


class IngestRunBody(BaseModel):
    """Si está vacío, usa DEFAULT_MICE_BATCH."""

    markets: list[MarketInput] | None = None


class IngestRunResponse(BaseModel):
    run_id: UUID
    status: str
    message: str


class BriefRequest(BaseModel):
    run_id: UUID | None = None
    send_whatsapp: bool = False


class BriefResponse(BaseModel):
    run_id: UUID
    data_as_of: datetime
    brief_text: str
    whatsapp_sent: bool = False
    whatsapp_detail: dict[str, Any] | None = None


class KapsoWebhookPayload(BaseModel):
    """Acepta cualquier JSON; Kapso puede enviar campos distintos."""

    model_config = {"extra": "allow"}
