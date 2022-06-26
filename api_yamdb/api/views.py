from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title, User, Review
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, SignUpSerializer,
                          AuthSerializer, UserSerializer,
                          ReviewSerializer, CommentsSerializer)

from .permissions import (IsOwnerModeratorAdminSuperuserOrReadOnly,
                          IsAdmin, IsAdminSuperuserOrReadOnly)


class TitleViewsSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminSuperuserOrReadOnly,)


class CategoryViewsSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminSuperuserOrReadOnly,)


class GenreViewsSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminSuperuserOrReadOnly,)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_fields = ('username',)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH',),
        permission_classes=[permissions.IsAuthenticated],
        url_path='me',
    )
    def profile(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method != 'PATCH':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(
            user,
            context={'request': request},
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if self.request.user.role == (
                user.is_admin or self.request.user.is_superuser
        ):
            serializer.save()
        else:
            serializer.save(role=user.role)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user = User.objects.create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения YaMDb',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email='admin@yamdb.com',
            recipient_list=[email]
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def auth(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.data.get('username')
    )
    confirmation_code = serializer.data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            str(token),
            status=status.HTTP_200_OK
        )
    return Response(
        status=status.HTTP_400_BAD_REQUEST
    )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerModeratorAdminSuperuserOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsOwnerModeratorAdminSuperuserOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
