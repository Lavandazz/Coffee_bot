from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "role" VARCHAR(20) NOT NULL DEFAULT 'user';
        ALTER TABLE "users" DROP COLUMN "is_admin";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "is_admin" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "users" DROP COLUMN "role";"""
