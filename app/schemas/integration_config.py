from pydantic import BaseModel


class IntegrationConfigCreate(BaseModel):
    provider_id: str
    config: dict


class IntegrationConfigRead(BaseModel):
    id: str
    provider_id: str
    config: dict
