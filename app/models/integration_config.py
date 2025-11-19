from sqlmodel import SQLModel, Field, Column, JSON
import uuid


class IntegrationConfig(SQLModel, table=True):
    __tablename__ = "integration_config"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    provider_id: uuid.UUID = Field(foreign_key="hrisprovider.id")

    config: dict = Field(sa_column=Column(JSON, nullable=False))
    is_active: bool = True
    created_at: str | None = None
    updated_at: str | None = None
