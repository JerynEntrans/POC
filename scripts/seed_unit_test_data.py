# from sqlmodel import Session
# from app.core.database import engine
# from app.models.hris_provider import HRISProvider
# from app.models.integration_config import IntegrationConfig
# import uuid


# def seed(schema: str = "public"):
#     """Seed initial data into the given schema."""
#     with Session(engine) as db:
#         # Set schema search path
#         db.exec(f"SET search_path TO {schema}, public")
#         db.info["schema"] = schema

#         # Example: create a sample HRIS provider
#         provider = HRISProvider(
#             id=uuid.uuid4(),
#             type="BAMBOOHR",
#             creds={"api_key": "test_key"},
#             is_active=True
#         )
#         db.add(provider)

#         # Example: create a sample integration config
#         config = IntegrationConfig(
#             provider_id=provider.id,
#             config={"sync_interval": "2h"},
#             is_active=True
#         )
#         db.add(config)

#         db.commit()
#         print(f"Seeded data in schema: {schema}")


# if __name__ == "__main__":
#     seed()  # You can pass a schema name if needed, e.g., seed("tenant1")
