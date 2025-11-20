from typing import Union
from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class HRISType(str, Enum):
    BAMBOOHR = "BAMBOOHR"
    # WORKDAY = "WORKDAY"
    # SAP_SUCCESSFACTORS = "SAP_SUCCESSFACTORS"
    # ADP = "ADP"
    # GUSTO = "GUSTO"
    # PAYCOR = "PAYCOR"
    # PAYCOM = "PAYCOM"


class BambooHRAPIConfig(BaseModel):
    api_key: str
    subdomain: str


class BambooHROAuth2Config(BaseModel):
    company_domain: str
    client_id: str
    client_secret: str


class HRISProviderCreate(BaseModel):
    type: HRISType
    config: Union[BambooHRAPIConfig, BambooHROAuth2Config]


class HRISProviderUpdate(BaseModel):
    type: HRISType
    config: Union[BambooHRAPIConfig, BambooHROAuth2Config]


class HRISProviderRead(BaseModel):
    id: UUID
    type: HRISType
    config: dict
