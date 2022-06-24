import re
from rest_framework import serializers

from reviews.models import User, Title, Genre, Category


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    def validate(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Запрещенное имя пользователя.'
            )
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError(
                ('Допустимые символы - латинский алфавит и '
                 'символы @ / . / + / - / _')
            )
        return username

    class Meta:
        model = User
        fields = ('username', 'email')


class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = (
            'confirmation_code',
            'username'
        )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class TitleSerializer(serializers.ModelSerializer):
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
        firlds = '__all__'
