import time
import uuid

import jwt

from core.config import settings
from schemas.auth import SessionPayload


def create_session_token() -> str:
    payload = SessionPayload(
        thread_id=str(uuid.uuid4()), exp=int(time.time()) + settings.session_ttl_seconds
    )
    return jwt.encode(payload.model_dump(), settings.jwt_secret, algorithm="HS256")


def decode_session_token(token: str) -> SessionPayload:
    data = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    return SessionPayload(**data)