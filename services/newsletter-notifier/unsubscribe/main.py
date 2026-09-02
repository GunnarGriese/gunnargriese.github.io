import hashlib
import hmac
import os

import functions_framework
from google.cloud import bigquery

CONFIRMATION_HTML = (
    "<!doctype html><html><body><p>You have been unsubscribed. "
    "You will not receive further newsletter emails.</p></body></html>"
)
ERROR_HTML = (
    "<!doctype html><html><body><p>This unsubscribe link is invalid or has expired.</p>"
    "</body></html>"
)


def _verify_token(email: str, token: str, secret: str) -> bool:
    # Duplicated from common/tokens.py: `gcloud functions deploy --source unsubscribe/`
    # only uploads this directory, so this handler can't import the sibling common/ package.
    expected = hmac.new(secret.encode("utf-8"), email.encode("utf-8"), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, token)


def mark_unsubscribed(bq_client: bigquery.Client, unsubscribes_table: str, email: str) -> None:
    query = f"""
        INSERT INTO `{unsubscribes_table}` (email, unsubscribed_at)
        VALUES (@email, CURRENT_TIMESTAMP())
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("email", "STRING", email)]
    )
    bq_client.query(query, job_config=job_config).result()


@functions_framework.http
def unsubscribe(request):
    email = request.args.get("email", "")
    token = request.args.get("token", "")
    secret = os.environ["UNSUBSCRIBE_SIGNING_KEY"]

    if not email or not token or not _verify_token(email, token, secret):
        return (ERROR_HTML, 400, {"Content-Type": "text/html"})

    bq_client = bigquery.Client()
    mark_unsubscribed(bq_client, os.environ["BQ_UNSUBSCRIBES_TABLE"], email)

    return (CONFIRMATION_HTML, 200, {"Content-Type": "text/html"})
