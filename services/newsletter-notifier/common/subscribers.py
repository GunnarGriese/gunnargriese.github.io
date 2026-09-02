from dataclasses import dataclass

from google.cloud import bigquery


@dataclass(frozen=True)
class Subscriber:
    email: str


def get_active_subscribers(
    bq_client: bigquery.Client, contacts_table: str, unsubscribes_table: str
) -> list[Subscriber]:
    query = f"""
        SELECT DISTINCT email
        FROM `{contacts_table}`
        WHERE message LIKE 'Newsletter signup from:%'
          AND email IS NOT NULL
          AND email NOT IN (SELECT email FROM `{unsubscribes_table}`)
    """
    rows = bq_client.query(query).result()
    return [Subscriber(email=row.email) for row in rows]
