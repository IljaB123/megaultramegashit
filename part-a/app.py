
import os
from contextlib import closing
import psycopg2


def connect_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=3
    )


def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")

    if path == "/healthz":
        status = "200 OK"
        message = "Healthy\n"

    elif path == "/readyz":
        try:
            with closing(connect_db()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")

            status = "200 OK"
            message = "Ready\n"

        except psycopg2.Error:
            status = "503 Service Unavailable"
            message = "Database unavailable\n"

    elif path == "/":
        with closing(connect_db()) as conn:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO visits DEFAULT VALUES")
                    cursor.execute("SELECT COUNT(*) FROM visits")
                    count = cursor.fetchone()[0]

        status = "200 OK"
        message = f"Total visits: {count}\n"

    else:
        status = "404 Not Found"
        message = "Not found\n"

    start_response(
        status,
        [("Content-Type", "text/plain; charset=utf-8")]
    )

    return [message.encode("utf-8")]
