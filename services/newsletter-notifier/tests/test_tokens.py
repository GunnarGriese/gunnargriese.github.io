from common.tokens import generate_token, verify_token


def test_generate_token_is_stable_for_same_email_and_secret():
    assert generate_token("reader@example.com", "secret") == generate_token(
        "reader@example.com", "secret"
    )


def test_generate_token_differs_for_different_emails():
    assert generate_token("a@example.com", "secret") != generate_token("b@example.com", "secret")


def test_generate_token_differs_for_different_secrets():
    assert generate_token("reader@example.com", "secret-one") != generate_token(
        "reader@example.com", "secret-two"
    )


def test_verify_token_accepts_a_token_generated_for_the_same_email_and_secret():
    token = generate_token("reader@example.com", "secret")
    assert verify_token("reader@example.com", token, "secret") is True


def test_verify_token_rejects_a_token_for_a_different_email():
    token = generate_token("reader@example.com", "secret")
    assert verify_token("someone-else@example.com", token, "secret") is False


def test_verify_token_rejects_a_tampered_token():
    token = generate_token("reader@example.com", "secret")
    tampered = token[:-1] + ("0" if token[-1] != "0" else "1")
    assert verify_token("reader@example.com", tampered, "secret") is False


def test_verify_token_rejects_a_token_signed_with_a_different_secret():
    token = generate_token("reader@example.com", "wrong-secret")
    assert verify_token("reader@example.com", token, "secret") is False


def test_verify_token_rejects_malformed_token():
    assert verify_token("reader@example.com", "not-a-real-token", "secret") is False
