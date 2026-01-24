from config.settings_env import settings

# настройка подключения к бд через TORTOISE
DATABASE_URL = (
    f"postgres://{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOST}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
)

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["database.models_db", "aerich.models"],  # aerich.models миграции
            "default_connection": "default",
        },
    },
}
