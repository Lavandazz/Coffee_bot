from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100)
    first_name = fields.CharField(max_length=100)
    telegram_id = fields.IntField(unique=True)
    role = fields.CharField(max_length=20, default='user')

    class Meta:
        table = 'users'


class AdminPost(Model):
    id = fields.IntField(pk=True)
    # models берется из config
    user_id: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User',
                                                                      related_name='posts',
                                                                      source_field="user_id")
    photo_file_id = fields.CharField(max_length=255)
    text = fields.TextField()
    date = fields.DatetimeField(auto_now_add=True)
    status = fields.IntField(default=0)

    class Meta:
        table = 'admin_posts'


class Review(Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User',
        related_name='reviews',
        db_column='user_id')
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
    test_text = fields.TextField(null=True)

    class Meta:
        table = "horoscopes"
        unique_together = ("zodiac", "date")  # Чтобы не было дублей


class Statistic(Model):
    id = fields.IntField(pk=True)
    day = fields.DateField()
    new_user = fields.IntField(default=0)
    event = fields.IntField(default=0)

    class Meta:
        table = 'statistic'

