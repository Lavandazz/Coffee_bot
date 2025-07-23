from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "registration_date" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "users" ALTER COLUMN "first_name" DROP NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "username" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "registration_date";
        ALTER TABLE "users" ALTER COLUMN "first_name" SET NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "username" SET NOT NULL;"""
