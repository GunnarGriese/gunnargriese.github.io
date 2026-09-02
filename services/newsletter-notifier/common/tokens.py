import hashlib
import hmac


def generate_token(email: str, secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), email.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_token(email: str, token: str, secret: str) -> bool:
    expected = generate_token(email, secret)
    return hmac.compare_digest(expected, token)
