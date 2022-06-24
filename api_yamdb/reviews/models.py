from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


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
    bio = models.TextField(
        blank=True,
        null=True,
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
        return self.role == 'admin' or self.is_superuser

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
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review')
        ]


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


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
