from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "review" DROP COLUMN "user_id";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "review" ADD "user_id" BIGINT NOT NULL;"""
