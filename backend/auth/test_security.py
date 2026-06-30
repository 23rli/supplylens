from auth.security import hash_password, verify_password, create_token, decode_token


def test_hash_roundtrip():
    h = hash_password("secret123")
    assert verify_password("secret123", h)
    assert not verify_password("wrong", h)


def test_hash_is_salted():
    assert hash_password("x") != hash_password("x")


def test_jwt_roundtrip():
    t = create_token({"id": 1, "email": "a@b.co", "tenant_id": "demo", "role": "admin"})
    claims = decode_token(t)
    assert claims["sub"] == "a@b.co"
    assert claims["tenant_id"] == "demo"
