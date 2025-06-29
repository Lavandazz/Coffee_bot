from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100)
    first_name = fields.CharField(max_length=100)
    telegram_id = fields.IntField(unique=True)
    is_admin = fields.BooleanField(default=False)

    class Meta:
        table = 'users'


class AdminPost(Model):
    id = fields.IntField(pk=True)
    # models берется из config
    user_id = fields.ForeignKeyField('models.User', related_name='posts', source_field="user_id")
    photo_file_id = fields.CharField(max_length=255)
    text = fields.TextField()
    date = fields.DatetimeField(auto_now_add=True)
    status = fields.IntField(default=0)

    class Meta:
        table = 'admin_posts'


class Review(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    username = fields.CharField(max_length=255, null=True)
    first_name = fields.CharField(max_length=255, null=True)
    photo_file_id = fields.CharField(max_length=255, null=True)
    text = fields.TextField(null=True)
    approved = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'review'


class Horoscope(Model):
    id = fields.IntField(pk=True)
    zodiac = fields.CharField(max_length=20)
    date = fields.DateField()
    text = fields.TextField()

    class Meta:
        table = "horoscopes"
        unique_together = ("zodiac", "date")  # Чтобы не было дублей
