from sqlmodel import SQLModel, Field, Column, JSON
import uuid


class IntegrationLog(SQLModel, table=True):
    __tablename__ = "integration_log"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    provider_id: uuid.UUID | None = Field(
        default=None, foreign_key="hrisprovider.id"
    )

    event_type: str
    message: str | None = None
    details: dict | None = Field(sa_column=Column(JSON))

    created_at: str | None = None
