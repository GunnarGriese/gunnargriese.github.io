from types import SimpleNamespace
from unittest.mock import MagicMock

from common.subscribers import Subscriber, get_active_subscribers

CONTACTS_TABLE = "project.dataset.contact_form"
UNSUBSCRIBES_TABLE = "project.dataset.newsletter_unsubscribes"


def make_bq_client(rows):
    bq_client = MagicMock()
    bq_client.query.return_value.result.return_value = rows
    return bq_client


def test_returns_a_subscriber_per_row():
    rows = [SimpleNamespace(email="a@example.com"), SimpleNamespace(email="b@example.com")]
    bq_client = make_bq_client(rows)

    subscribers = get_active_subscribers(bq_client, CONTACTS_TABLE, UNSUBSCRIBES_TABLE)

    assert subscribers == [Subscriber(email="a@example.com"), Subscriber(email="b@example.com")]


def test_returns_empty_list_when_no_rows():
    bq_client = make_bq_client([])

    assert get_active_subscribers(bq_client, CONTACTS_TABLE, UNSUBSCRIBES_TABLE) == []


def test_query_filters_by_newsletter_signup_message_prefix():
    bq_client = make_bq_client([])

    get_active_subscribers(bq_client, CONTACTS_TABLE, UNSUBSCRIBES_TABLE)

    query = bq_client.query.call_args[0][0]
    assert "message LIKE 'Newsletter signup from:%'" in query


def test_query_excludes_unsubscribed_emails():
    bq_client = make_bq_client([])

    get_active_subscribers(bq_client, CONTACTS_TABLE, UNSUBSCRIBES_TABLE)

    query = bq_client.query.call_args[0][0]
    assert f"NOT IN (SELECT email FROM `{UNSUBSCRIBES_TABLE}`)" in query


def test_query_selects_distinct_email_from_contacts_table():
    bq_client = make_bq_client([])

    get_active_subscribers(bq_client, CONTACTS_TABLE, UNSUBSCRIBES_TABLE)

    query = bq_client.query.call_args[0][0]
    assert "SELECT DISTINCT email" in query
    assert f"FROM `{CONTACTS_TABLE}`" in query


def test_query_includes_a_partition_filter_on_timestamp():
    # contact_form is day-partitioned on `timestamp` with require_partition_filter=True;
    # an unfiltered query is rejected by BigQuery, so this must always be present.
    bq_client = make_bq_client([])

    get_active_subscribers(bq_client, CONTACTS_TABLE, UNSUBSCRIBES_TABLE)

    query = bq_client.query.call_args[0][0]
    assert "timestamp <= CURRENT_TIMESTAMP()" in query
