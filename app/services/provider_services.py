from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.models.hris_provider import HRISProvider
from app.schemas.hris_provider import HRISProviderCreate


def create_provider(db: Session, provider: HRISProviderCreate):
    new_provider = HRISProvider(
        type=provider.type,
        creds=provider.creds,
        is_active=True
    )
    db.add(new_provider)

    try:
        db.commit()
        db.refresh(new_provider)
        return new_provider

    except IntegrityError as e:
        db.rollback()

        if "unique_active_hris_provider" in str(e.orig):
            # Fetch existing active provider
            existing: HRISProvider = db.exec(
                select(HRISProvider).where(HRISProvider.is_active.is_(True))).scalar_one_or_none()

            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Active provider already exists",
                    "message": "Deactivate the existing integration before creating a new one.",
                    "existing_provider_id": str(existing.id),
                    "existing_provider_type": existing.type,
                }
            )

        raise e
