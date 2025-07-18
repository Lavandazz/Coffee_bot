from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "statistic" ALTER COLUMN "day" TYPE DATE USING "day"::DATE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "statistic" ALTER COLUMN "day" TYPE TIMESTAMPTZ USING "day"::TIMESTAMPTZ;"""
