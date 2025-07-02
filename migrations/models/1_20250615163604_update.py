from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "admin_posts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "photo_file_id" VARCHAR(255) NOT NULL,
    "text" TEXT NOT NULL,
    "date" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "status" INT NOT NULL DEFAULT 0,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "review" (
    "id" SERIAL NOT NULL PRIMARY KEY,

    "username" VARCHAR(255),
    "first_name" VARCHAR(255),
    "photo_file_id" VARCHAR(255),
    "text" TEXT,
    "approved" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
        DROP TABLE IF EXISTS "posts";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "admin_posts";
        DROP TABLE IF EXISTS "review";"""
