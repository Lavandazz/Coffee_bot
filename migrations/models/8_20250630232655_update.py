from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "review" ADD "user_id" INT NOT NULL;
        ALTER TABLE "review" ADD CONSTRAINT "fk_review_users_5086ac2b" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "review" DROP CONSTRAINT IF EXISTS "fk_review_users_5086ac2b";
        ALTER TABLE "review" DROP COLUMN "user_id";"""
