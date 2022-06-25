from rest_framework import serializers

from reviews.models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
