from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "static" RENAME TO "statistic";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "statistic" RENAME TO "static";"""
