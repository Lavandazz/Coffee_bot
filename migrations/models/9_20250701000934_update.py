from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "horoscopes" ADD "test_text" TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "horoscopes" DROP COLUMN "test_text";"""
