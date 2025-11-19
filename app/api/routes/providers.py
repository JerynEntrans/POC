from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_db
from app.schemas.hris_provider import HRISProviderCreate, HRISProviderRead
from app.services.provider_services import create_provider

router = APIRouter(prefix="/provider", tags=["provider"])


@router.post("/", response_model=HRISProviderRead)
def create_provider_endpoint(
    data: HRISProviderCreate,
    db: Session = Depends(get_db)
):
    return create_provider(db, data)
