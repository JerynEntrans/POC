# from fastapi import HTTPException
from fastapi import HTTPException
from app.clients.bamboohr import BambooHRClient
from app.models.hris_provider import HRISProvider
from app.models.integration_log import IntegrationLog
from sqlmodel import Session, select

# from app.schemas.integration_config import IntegrationConfigCreate


def get_active_provider(db: Session) -> HRISProvider | None:
    """Returns the currently active HRIS provider, if any."""
    return db.exec(
        select(HRISProvider).where(HRISProvider.is_active.is_(True))
    ).first()


# def get_active_config(db: Session, provider_id) -> IntegrationConfig | None:
#     """Returns the active integration config for the given provider."""
#     return db.exec(
#         select(IntegrationConfig)
#         .where(
#             IntegrationConfig.provider_id == provider_id,
#             IntegrationConfig.is_active.is_(True)
#         )
#     ).first()


def get_client(provider_type: str):
    if provider_type == "BAMBOOHR":
        return BambooHRClient()
    raise ValueError(f"Unsupported provider type: {provider_type}")


def run_sync(db: Session, provider: HRISProvider, raise_on_error=False):
    client = get_client(provider.type.value)

    try:
        result = client.sync(provider, db)

        log = IntegrationLog(
            provider_id=provider.id,
            event_type="SYNC_COMPLETED",
            details={"records": len(result)}
        )
        db.add(log)
        db.commit()

        return result

    except Exception as e:
        # ERROR LOG
        log = IntegrationLog(
            provider_id=provider.id,
            event_type="SYNC_FAILED",
            message=str(e)
        )
        db.add(log)
        db.commit()
        if raise_on_error:
            raise HTTPException(status_code=500, detail=f"Sync failed: {e}")


# def create_integration_config(db: Session, data: IntegrationConfigCreate) -> IntegrationConfig:
#     # If new config is_active, ensure provider has no other active config
#     if data.is_active:
#         q = select(IntegrationConfig).where(
#             IntegrationConfig.provider_id == data.provider_id,
#             IntegrationConfig.is_active.is_(True)
#             )
#     existing = db.exec(q).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="There is already an active config for this provider.")

#     config = IntegrationConfig.model_validate(data)
#     db.add(config)
#     db.commit()
#     db.refresh(config)
#     return config
