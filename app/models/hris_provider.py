from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional
import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import func


class HRISType(str, Enum):
    BAMBOOHR = "BAMBOOHR"
    # WORKDAY = "WORKDAY"
    # SAP_SUCCESSFACTORS = "SAP_SUCCESSFACTORS"
    # ADP = "ADP"
    # GUSTO = "GUSTO"
    # PAYCOR = "PAYCOR"
    # PAYCOM = "PAYCOM"


class HRISProvider(SQLModel, table=True):
    __tablename__ = "hris_provider"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: HRISType
    config: dict = Field(sa_column=Column(JSON, nullable=False))

    is_active: bool = True

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            nullable=False,
            server_default=func.now(),
        ),
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )
