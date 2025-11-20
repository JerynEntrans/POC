from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session
from app.core.database import get_db
from app.schemas.hris_provider import HRISProviderCreate, HRISProviderRead
from app.services.provider_services import create_provider, delete_provider, get_active_provider, get_provider_by_id

router = APIRouter(prefix="/provider", tags=["provider"])


@router.post("/", response_model=HRISProviderRead)
def create_provider_endpoint(
    data: HRISProviderCreate,
    db: Session = Depends(get_db)
):
    return create_provider(db, data)


@router.get("/active-provider", response_model=HRISProviderRead)
def get_active_provider_endpoint(
    db: Session = Depends(get_db),
):
    provider = get_active_provider(db)
    if not provider:
        raise HTTPException(
                status_code=400,
                detail={
                    "error": "Active provider does not exists",
                    "message": "Create a new one."
                }
            )
    return provider


@router.get("/{provider_id}", response_model=HRISProviderRead)
def get_provider_endpoint(
    db: Session = Depends(get_db),
    provider_id: UUID = Path(..., description="ID of the provider to retrieve"),
):
    provider = get_provider_by_id(db, provider_id)
    if not provider:
        raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Provider with ID - {provider_id} does not exists",
                    "message": "Create a new one."
                }
            )
    return provider


@router.delete("/{provider_id}", response_model=HRISProviderRead)
def delete_provider_endpoint(
    provider_id: UUID = Path(..., description="ID of the provider to retrieve"),
    db: Session = Depends(get_db)
):
    return delete_provider(db, provider_id)
