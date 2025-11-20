from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class HRISType(str, Enum):
    BAMBOOHR = "BAMBOOHR"


class HRISProviderCreate(BaseModel):
    type: HRISType
    creds: dict


class HRISProviderUpdate(BaseModel):
    type: Optional[HRISType] = None
    creds: Optional[dict] = None


class HRISProviderRead(BaseModel):
    id: UUID
    type: HRISType
    creds: dict
