from app.clients.bamboohr import BambooHRClient
from app.models.hris_provider import HRISProvider
from app.models.integration_config import IntegrationConfig
from app.models.integration_log import IntegrationLog
from sqlmodel import Session, select


def get_active_provider(db: Session) -> HRISProvider | None:
    """Returns the currently active HRIS provider, if any."""
    return db.exec(
        select(HRISProvider).where(HRISProvider.is_active.is_(True))
    ).first()


def get_active_config(db: Session, provider_id) -> IntegrationConfig | None:
    """Returns the active integration config for the given provider."""
    return db.exec(
        select(IntegrationConfig)
        .where(
            IntegrationConfig.provider_id == provider_id,
            IntegrationConfig.is_active.is_(True)
        )
    ).first()


def get_client(provider_type: str):
    if provider_type == "BAMBOOHR":
        return BambooHRClient()
    raise ValueError(f"Unsupported provider type: {provider_type}")


def run_sync(db: Session, provider: HRISProvider, config: IntegrationConfig):
    """Run the sync for a provider and log results."""
    client = get_client(provider.type.value)
    try:
        result = client.sync(provider, config.config)

        log = IntegrationLog(
            provider_id=provider.id,
            event_type="SYNC_COMPLETED",
            details={"records": len(result)}
        )
        db.add(log)
        db.commit()

        return result

    except Exception as e:
        log = IntegrationLog(
            provider_id=provider.id,
            event_type="SYNC_FAILED",
            message=str(e)
        )
        db.add(log)
        db.commit()
        raise
