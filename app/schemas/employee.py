from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class EmployeeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    provider_id: UUID
    employee_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    work_email: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    preferred_name: Optional[str] = None
    display_name: Optional[str] = None
    supervisor: Optional[str] = None
    division: Optional[str] = None
    work_phone: Optional[str] = None
    photo_url: Optional[str] = None
    work_phone_extension: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class EmployeeUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    work_email: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    preferred_name: Optional[str] = None
    display_name: Optional[str] = None
    supervisor: Optional[str] = None
    division: Optional[str] = None
    work_phone: Optional[str] = None
    work_phone_extension: Optional[str] = None
    photo_url: Optional[str] = None
