from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_db
from app.services.sync_service import get_active_provider, run_sync

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/manual")
def manual_sync(db: Session = Depends(get_db)):
    provider = get_active_provider(db)
    if not provider:
        raise HTTPException(status_code=404, detail="No active HRIS provider found")

    return run_sync(db, provider)


# @router.post("/config", response_model=IntegrationConfigRead)
# def create_config(data: IntegrationConfigCreate, db: Session = Depends(get_db)) -> IntegrationConfigRead:
#     return create_integration_config(db, data)


# @router.delete("/config/{provider_id}/{integration_id}", response_model=IntegrationConfigRead)
# def delete_config(provider_id, integration_id, db: Session = Depends(get_db)) -> IntegrationConfigRead:
#     return create_integration_config(db, data)


# @router.get("/config/active/{provider_id}", response_model=IntegrationConfigRead)
# def get_active_config_for_provider(provider_id, db: Session = Depends(get_db)):
#     config = get_active_config(db, provider_id)
#     if not config:
#         raise HTTPException(status_code=404, detail="No active integration config found")
#     return config
