from django.db import models


class User(models.Model):
    pass


class Review(models.Model):
    pass


class Comment(models.Model):
    pass


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
        related_name='titles'
    )
    description = models.CharField(max_length=100)
