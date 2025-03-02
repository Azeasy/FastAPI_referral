from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from alembic import context
from src.core.config import settings
from src.db.base import Base
from src.models import referral
from src.models import user

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# get the database URL from the environment variable
database_url = settings.DATABASE_URL
if database_url is None:
    raise ValueError("DATABASE_URL environment variable is not set")

config.set_main_option('sqlalchemy.url', database_url)

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode using an async database connection."""
    # Create async engine
    connectable: AsyncEngine = create_async_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    if isinstance(connectable, AsyncEngine):
        await run_async_migrations(connectable)
    else:
        do_run_migrations(connectable)


async def run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
