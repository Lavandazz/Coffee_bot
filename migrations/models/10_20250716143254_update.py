from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "static" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "day" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "new_user" INT NOT NULL DEFAULT 0,
    "event" INT NOT NULL DEFAULT 0
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "static";"""
