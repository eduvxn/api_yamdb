from audioop import avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from reviews.models import User, Title, Genre, Category, Comments, Review


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    def validate(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Запрещенное имя пользователя.'
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


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценкой может быть целое число в диапазоне от 1 до 10.'
            )
        return value


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
        read_only_fields = ("author",)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(many=True, read_only=True)
    rating = serializers.SerializerMethodField()


    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(avg('score')).get('score__avg')
        if not rating:
            return rating
        return round(rating, 1)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
