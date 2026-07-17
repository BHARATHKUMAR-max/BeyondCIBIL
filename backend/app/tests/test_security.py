import uuid

import pytest

from app.core.security import (
    TokenValidationError,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_password_hashing_uses_bcrypt() -> None:
    password_hash = hash_password("StrongPass123!")

    assert password_hash.startswith("$2")
    assert verify_password("StrongPass123!", password_hash)
    assert not verify_password("incorrect-password", password_hash)


def test_tokens_enforce_their_expected_type() -> None:
    user_id = uuid.uuid4()
    access_token = create_access_token(user_id)
    refresh_token, _ = create_refresh_token(user_id, uuid.uuid4())

    assert decode_token(access_token, "access")["sub"] == str(user_id)
    assert decode_token(refresh_token, "refresh")["sub"] == str(user_id)
    with pytest.raises(TokenValidationError):
        decode_token(access_token, "refresh")
