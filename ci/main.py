import sys

import anyio
import dagger
from loguru import logger

WORKDIR = "/app"
POSTGRES_PASSWORD = "password"
POSTGRES_DB = "db"
POETRY_CACHE_DIR = "/poetry_cache"


async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        pg = (
            client.container()
            .from_("postgres:14")
            .with_env_variable("POSTGRES_PASSWORD", POSTGRES_PASSWORD)
            .with_env_variable("POSTGRES_DB", POSTGRES_DB)
            .with_exposed_port(5432)
        )

        poetry_cache = client.cache_volume("poetry")

        sqlmesh = (
            client.container()
            .from_("python:3.10-slim-buster")
            .with_mounted_directory(WORKDIR, client.host().directory("."))
            .with_workdir(WORKDIR)
            .with_mounted_cache(POETRY_CACHE_DIR, poetry_cache)
            .with_exec(["apt", "update"])
            .with_exec(["apt", "install", "-y", "gcc", "libpq-dev"])
            .with_exec(["pip", "install", "--upgrade", "pip"])
            .with_exec(["pip", "install", "--no-cache-dir", "poetry==1.3.0"])
            .with_env_variable("POETRY_VIRTUALENVS_CREATE", "false")
            .with_env_variable("POETRY_VIRTUALENVS_IN_PROJECT", "false")
            .with_env_variable("POETRY_CACHE_DIR", POETRY_CACHE_DIR)
            .with_exec(["poetry", "install"])
        )

        # service binding for Postgres
        test = await (
            sqlmesh.with_service_binding("localhost", pg)
            .with_exec(["yoyo", "apply", "--batch"])
            .with_exec(["python", "scripts/schema_converter.py", "bq2pg"])
            .with_env_variable("SQLMESH_DEBUG", "1")
            .with_exec(["sqlmesh", "--gateway", "ci", "create_external_models"])
            .with_exec(["python", "scripts/schema_augmenter.py"])
            .with_exec(["ls", "-lsa"])
            .with_exec(["cat", "schema.yaml"])
            .with_exec(["sqlmesh", "--gateway", "ci", "plan", "--no-prompts"])
        )

    # print ref
    logger.info(test)


anyio.run(main)
