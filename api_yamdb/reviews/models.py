from django.contrib.auth.models import AbstractUser
from django.db import models


roles = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    """Модель пользователя"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_superuser:
            self.role = 'admin'

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Ник пользователя',
        db_index=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='Фамилия пользователя'
    )
    bio = models.CharField(
        blank=True,
        verbose_name='Информация о себе'
    )
    role = models.CharField(
        max_length=50,
        default='user',
        choices=roles,
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        blank=True,
        verbose_name='Код подтверждения учетной записи',
    )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'moderator' or self.is_superuser

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]

    def __str__(self):
        return self.username


class Review(models.Model):
    pass


class Comment(models.Model):
    pass


class Category(models.Model):
    name = models.CharField()
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField()
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField()
    year = models.IntegerField()
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='titles',
        unique=True
    )
    description = models.CharField()
