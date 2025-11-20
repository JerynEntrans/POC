from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Column, UniqueConstraint
from sqlalchemy import func


class Employee(SQLModel, table=True):
    __tablename__ = "employee"

    __table_args__ = (
        UniqueConstraint("provider_id", "employee_id"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    provider_id: UUID = Field(
        foreign_key="hris_provider.id",
        nullable=False
    )

    employee_id: str = Field(nullable=False, max_length=50)

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    preferred_name: Optional[str] = None
    display_name: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    supervisor: Optional[str] = None
    department: Optional[str] = None
    division: Optional[str] = None
    work_email: Optional[str] = None
    work_phone: Optional[str] = None
    work_phone_extension: Optional[str] = None
    photo_url: Optional[str] = None

    created_at: datetime | None = Field(
        sa_column=Column(
            nullable=False,
            server_default=func.now()
        )
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            nullable=False,
            server_default=func.now(),
            onupdate=func.now()
        )
    )
