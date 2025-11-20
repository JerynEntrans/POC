# from datetime import datetime
# from typing import Optional
# from sqlmodel import SQLModel, Field, Column, JSON
# import uuid
# from sqlalchemy import func


# class IntegrationConfig(SQLModel, table=True):
#     __tablename__ = "integration_config"

#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     provider_id: uuid.UUID = Field(foreign_key="hris_provider.id")

#     config: dict = Field(sa_column=Column(JSON, nullable=False))
#     is_active: bool = True

#     created_at: Optional[datetime] = Field(
#         default=None,
#         sa_column=Column(
#             nullable=False,
#             server_default=func.now(),
#         ),
#     )

#     updated_at: Optional[datetime] = Field(
#         default=None,
#         sa_column=Column(
#             nullable=False,
#             server_default=func.now(),
#             onupdate=func.now(),
#         ),
#     )
