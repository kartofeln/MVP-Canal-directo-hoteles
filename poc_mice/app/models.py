import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(32), default="pending")
    error_message: Mapped[str | None] = mapped_column(Text)
    meta: Mapped[dict | None] = mapped_column(JSON)

    snapshots: Mapped[list["KeywordSnapshot"]] = relationship(
        "KeywordSnapshot", back_populates="run"
    )


class KeywordSnapshot(Base):
    __tablename__ = "keyword_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("ingestion_runs.id"), index=True
    )
    market_label: Mapped[str] = mapped_column(String(128))
    location_code: Mapped[int] = mapped_column(Integer)
    language_code: Mapped[str] = mapped_column(String(8))
    keyword: Mapped[str] = mapped_column(String(512))
    search_volume: Mapped[int | None] = mapped_column(Integer)
    competition: Mapped[float | None] = mapped_column(Float)
    cpc: Mapped[float | None] = mapped_column(Float)
    raw_item: Mapped[dict | None] = mapped_column(JSON)

    run: Mapped["IngestionRun"] = relationship("IngestionRun", back_populates="snapshots")
