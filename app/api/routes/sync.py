from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_db
from app.services.sync_service import get_active_provider, get_active_config, run_sync

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/manual")
def manual_sync(db: Session = Depends(get_db)):
    provider = get_active_provider(db)
    if not provider:
        raise HTTPException(status_code=404, detail="No active HRIS provider found")

    config = get_active_config(db, provider.id)
    if not config:
        raise HTTPException(status_code=404, detail="No active integration config found")

    return run_sync(db, provider, config)
