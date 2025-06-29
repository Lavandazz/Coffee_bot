from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "horoscopes" DROP CONSTRAINT IF EXISTS "uid_horoscopes_zodiac_71cfe1";
        ALTER TABLE "horoscopes" ADD "date" DATE NOT NULL;
        ALTER TABLE "horoscopes" DROP COLUMN "month";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_horoscopes_zodiac_ad23b6" ON "horoscopes" ("zodiac", "date");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_horoscopes_zodiac_ad23b6";
        ALTER TABLE "horoscopes" ADD "month" VARCHAR(10) NOT NULL;
        ALTER TABLE "horoscopes" DROP COLUMN "date";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_horoscopes_zodiac_71cfe1" ON "horoscopes" ("zodiac", "month");"""
