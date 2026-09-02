import ast
from pathlib import Path
from unittest.mock import MagicMock

from common.tokens import generate_token
from unsubscribe.main import mark_unsubscribed, unsubscribe

MAIN_PATH = Path(__file__).parent.parent / "unsubscribe" / "main.py"

SECRET = "secret"
UNSUBSCRIBES_TABLE = "project.dataset.newsletter_unsubscribes"


def make_request(email=None, token=None):
    args = {}
    if email is not None:
        args["email"] = email
    if token is not None:
        args["token"] = token
    return MagicMock(args=args)


def set_env(monkeypatch):
    monkeypatch.setenv("UNSUBSCRIBE_SIGNING_KEY", SECRET)
    monkeypatch.setenv("BQ_UNSUBSCRIBES_TABLE", UNSUBSCRIBES_TABLE)


def test_main_does_not_import_the_sibling_common_package():
    # `gcloud functions deploy --source unsubscribe/` only uploads this directory,
    # so an import reaching into ../common would ImportError in production.
    tree = ast.parse(MAIN_PATH.read_text())
    imported_modules = [
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    ] + [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module]

    assert not any(
        module == "common" or module.startswith("common.") for module in imported_modules
    )


def test_mark_unsubscribed_uses_a_parameterized_query_not_string_interpolation():
    bq_client = MagicMock()
    email = "reader@example.com"

    mark_unsubscribed(bq_client, UNSUBSCRIBES_TABLE, email)

    query = bq_client.query.call_args[0][0]
    assert email not in query
    job_config = bq_client.query.call_args.kwargs["job_config"]
    param = job_config.query_parameters[0]
    assert param.name == "email"
    assert param.value == email


def test_valid_token_marks_the_row_unsubscribed_and_returns_confirmation(monkeypatch, mocker):
    set_env(monkeypatch)
    email = "reader@example.com"
    token = generate_token(email, SECRET)
    fake_bq_client = MagicMock()
    mocker.patch("unsubscribe.main.bigquery.Client", return_value=fake_bq_client)

    body, status, _headers = unsubscribe(make_request(email=email, token=token))

    assert status == 200
    assert "unsubscribed" in body.lower()
    query = fake_bq_client.query.call_args[0][0]
    assert f"`{UNSUBSCRIBES_TABLE}`" in query
    job_config = fake_bq_client.query.call_args.kwargs["job_config"]
    assert job_config.query_parameters[0].value == email


def test_invalid_token_returns_error_without_mutating_data(monkeypatch, mocker):
    set_env(monkeypatch)
    fake_bq_client = MagicMock()
    mocker.patch("unsubscribe.main.bigquery.Client", return_value=fake_bq_client)

    body, status, _headers = unsubscribe(make_request(email="reader@example.com", token="tampered"))

    assert status == 400
    fake_bq_client.query.assert_not_called()


def test_missing_email_or_token_returns_error_without_mutating_data(monkeypatch, mocker):
    set_env(monkeypatch)
    fake_bq_client = MagicMock()
    mocker.patch("unsubscribe.main.bigquery.Client", return_value=fake_bq_client)

    body, status, _headers = unsubscribe(make_request(email=None, token=None))

    assert status == 400
    fake_bq_client.query.assert_not_called()


def test_token_valid_for_a_different_email_is_rejected(monkeypatch, mocker):
    set_env(monkeypatch)
    token = generate_token("someone-else@example.com", SECRET)
    fake_bq_client = MagicMock()
    mocker.patch("unsubscribe.main.bigquery.Client", return_value=fake_bq_client)

    body, status, _headers = unsubscribe(make_request(email="reader@example.com", token=token))

    assert status == 400
    fake_bq_client.query.assert_not_called()
