from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "horoscopes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "zodiac" VARCHAR(20) NOT NULL,
    "month" VARCHAR(10) NOT NULL,
    "text" TEXT NOT NULL,
    CONSTRAINT "uid_horoscopes_zodiac_71cfe1" UNIQUE ("zodiac", "month")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "horoscopes";"""
