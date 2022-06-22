from rest_framework import serializers


from reviews.models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):
    class meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class meta:
        model = Category
        firlds = '__all__'
