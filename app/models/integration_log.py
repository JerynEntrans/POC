from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlmodel import SQLModel, Field, Column, JSON
import uuid


class IntegrationLog(SQLModel, table=True):
    __tablename__ = "integration_logs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    provider_id: uuid.UUID | None = Field(
        default=None, foreign_key="hris_provider.id"
    )

    event_type: str
    message: str | None = None
    details: dict | None = Field(sa_column=Column(JSON))

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            nullable=False,
            server_default=func.now(),
        ),
    )
