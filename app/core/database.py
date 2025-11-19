from sqlmodel import Session, create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import text
from fastapi import Depends

# from app.services.external_services.external_auth import JWTAuthorizationCredentials, auth

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'local')}:{os.getenv('POSTGRES_PASSWORD', 'test')}@{os.getenv('DATABASE_HOST', 'mesh-db-local')}:5432/{os.getenv('POSTGRES_DB', 'mesh_db_local')}"

engine = create_engine(DATABASE_URL, echo=True)


def get_db_with_schema(schema: str = "public"):
    with Session(engine) as db:
        db.exec(text(f"SET search_path TO {schema}, public"))
        db.info["schema"] = schema
        yield db


def extract_schema_from_token(
        # jwt_credentials: JWTAuthorizationCredentials = Depends(auth)
        ) -> str:
    return "public"  # TODO: Fix this to extract from JWT
    # return jwt_credentials.claims.get("tenant", "public")


def get_db(schema: str = Depends(extract_schema_from_token)):
    yield from get_db_with_schema(schema=schema)


def reset_schema(db):
    schema = db.info.get("schema")
    if schema:
        db.exec(text(f"SET search_path TO {schema}"))
