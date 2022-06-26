from django.contrib.auth.models import AbstractUser

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


roles = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    """Модель пользователя"""

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


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=20)
    search_fields = ['slug']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=20)
    search_fields = ['slug']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=20)
    year = models.IntegerField()
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='titles',
        null=True,
        blank=True
    )
    description = models.CharField(max_length=100, null=True)


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор')
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
        User, on_delete=models.CASCADE,
        related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
