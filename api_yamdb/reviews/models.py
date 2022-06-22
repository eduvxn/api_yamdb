from django.db import models


class User(models.Model):
    pass


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
    categoriy = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='titles',
        unique=True
    )
    description = models.CharField()