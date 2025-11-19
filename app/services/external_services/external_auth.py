import os
from typing import Any, Dict, Optional, List, Callable

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, jwk, JWTError
from jose.utils import base64url_decode
from pydantic import BaseModel
import requests
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from utils.set_logging import set_logging
logger = set_logging("external_auth")


class JWTAuthorizationCredentials(BaseModel):
    jwt_token: str
    header: Dict[str, Any]
    claims: Dict[str, Any]
    signature: str
    message: str


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[JWTAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials or credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid authentication method")

        jwt_token = credentials.credentials
        try:
            header = jwt.get_unverified_header(jwt_token)
            access_claims = jwt.get_unverified_claims(jwt_token)
            message, signature = jwt_token.rsplit(".", 1)
        except JWTError:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid JWT format")

        issuer = access_claims.get("iss")
        if not issuer:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Issuer missing in token")

        # Determine JWKS URL based on issuer
        if "unifed" in issuer:
            jwks_url = f"{os.environ['UNIFED_JWKS_BASE_URL']}{os.environ['MESH_UNIFED_TENANT_ID']}/{os.environ['UNIFED_JWKS_SUFFIX']}"
        # NOTE: Pipeline and other services use cognito here
        elif "cognito-idp" in issuer:
            jwks_url = f"{os.environ['COGNITO_URL']}{os.environ['COGNITO_POOL_ID']}/.well-known/jwks.json"
        else:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=f"Unknown issuer {issuer}")

        try:
            jwks_data = requests.get(jwks_url, timeout=5).json()
            kid_to_jwk = {jwk_obj["kid"]: jwk_obj for jwk_obj in jwks_data["keys"]}
            public_key = kid_to_jwk[header["kid"]]
        except Exception as e:
            logger.error(f"Failed to fetch or match JWK: {e}")
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="JWK public key not found or invalid")

        try:
            key = jwk.construct(public_key)
            decoded_signature = base64url_decode(signature.encode())
            if not key.verify(message.encode(), decoded_signature):
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid token signature")
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token signature verification failed")

        #  Now check for ID token if present
        id_token = request.headers.get("id_token")
        id_claims = {}
        if id_token:
            try:
                id_claims = jwt.get_unverified_claims(id_token)
            except JWTError:
                logger.warning("Invalid ID token format, ignoring")

        # Merge claims (access token takes precedence)
        combined_claims = {**id_claims, **access_claims}

        # Extract tenant_id - check both tokens and different claim names
        tenant_id = (
            access_claims.get("tenant") or  # this is for unifed token
            id_claims.get("custom:tenant_id") or  # this is for cognito id_token
            "public"
        )
        combined_claims["tenant"] = tenant_id

        return JWTAuthorizationCredentials(
            jwt_token=jwt_token,
            header=header,
            claims=combined_claims,
            signature=signature,
            message=message,
        )


auth = JWTBearer()


def scope_required(required_scopes: List[str]) -> Callable:
    def verify_scopes(jwt_credentials: Optional[JWTAuthorizationCredentials] = Depends(auth)) -> None:
        if jwt_credentials is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid authentication credentials")

        token_scopes = jwt_credentials.claims.get("scope", "").split()
        missing_scopes = [scope for scope in required_scopes if scope not in token_scopes]

        if missing_scopes:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"User not authorized for this action. Missing scope(s): {', '.join(missing_scopes)}"
            )
    return verify_scopes
