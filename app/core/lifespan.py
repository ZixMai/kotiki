from contextlib import asynccontextmanager
from os import environ
from dotenv import find_dotenv, load_dotenv
import aioboto3
from psycopg_pool import AsyncConnectionPool
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    if find_dotenv():
        load_dotenv()

    is_docker = environ["PYTHON_ENV"] == "DOCKER"

    s3_access_key = environ.get("S3_ACCESS_KEY", "admin")
    s3_secret_key = environ.get("S3_SECRET_KEY", "adminsecret")

    s3_settings = {
        "endpoint_url": f"http://{environ['S3_DOCKER_HOST'] if is_docker else 'localhost'}:8333",
        "aws_access_key_id": s3_access_key,
        "aws_secret_access_key": s3_secret_key,
        "region_name": "us-east-1",
        "bucket": "files",
    }

    conninfo = (
        "host="
        + (environ["POSTGRES_DOCKER_HOST"] if is_docker else "localhost")
        + " port=5432"
        + f" dbname={environ['POSTGRES_PGDB']}"
        + f" user={environ['POSTGRES_PGUSER']}"
        + f" password={environ['POSTGRES_PGPASS']}"
    )
    pg_pool = AsyncConnectionPool(conninfo=conninfo, min_size=1, max_size=20)
    await pg_pool.open()

    app.state.s3_session = aioboto3.Session()
    app.state.s3_settings = s3_settings
    app.state.pg_pool = pg_pool

    try:
        yield
    finally:
        await pg_pool.close()
