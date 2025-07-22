from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "horoscopes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "zodiac" VARCHAR(20) NOT NULL,
    "date" DATE NOT NULL,
    "text" TEXT NOT NULL,
    "test_text" TEXT,
    CONSTRAINT "uid_horoscopes_zodiac_ad23b6" UNIQUE ("zodiac", "date")
);
CREATE TABLE IF NOT EXISTS "statistic" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "day" DATE NOT NULL,
    "new_user" INT NOT NULL DEFAULT 0,
    "event" INT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL,
    "first_name" VARCHAR(100) NOT NULL,
    "telegram_id" BIGINT NOT NULL UNIQUE,
    "role" VARCHAR(20) NOT NULL DEFAULT 'user'
);
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
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
