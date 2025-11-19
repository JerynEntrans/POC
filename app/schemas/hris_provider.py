from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class HRISType(str, Enum):
    BAMBOOHR = "BAMBOOHR"


class HRISProviderCreate(BaseModel):
    type: HRISType
    creds: dict


class HRISProviderRead(BaseModel):
    id: UUID
    type: HRISType
    creds: dict
