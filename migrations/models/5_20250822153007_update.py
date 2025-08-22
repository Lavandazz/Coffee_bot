from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "game" ADD "status" VARCHAR(20) NOT NULL DEFAULT 'to be';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "game" DROP COLUMN "status";"""
