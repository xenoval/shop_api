from auth.security import (
    get_password_hash, verify_password,
    create_access_token, decode_access_token,
)


def test_hash_and_verify():
    hashed = get_password_hash("secret123")
    assert hashed != "secret123"
    assert verify_password("secret123", hashed) is True
    assert verify_password("wrong", hashed) is False


def test_create_and_decode_token():
    token = create_access_token({"sub": "abc"})
    payload = decode_access_token(token)
    assert payload["sub"] == "abc"
    assert "exp" in payload