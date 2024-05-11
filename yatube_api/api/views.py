"""Представления для работы с моделями приложения API."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Comment, Follow, Group
from .serializers import (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer
)
from .permissions import IsOwnerOrReadOnly


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Представление для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создание записи с указанием автора и группы."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object_post(self):
        """Функция для создания поста."""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Получение записи авторизированным пользователем."""
        post_id = self.kwargs.get('post_id')
        post = self.get_object_post()
        return post.comments.filter(post_id=post_id)

    def perform_create(self, serializer):
        """Создание записи без указания номера поста и автора в запросе."""
        post_id = self.kwargs.get('post_id')
        self.get_object_post()
        serializer.save(
            author_id=self.request.user.id,
            post_id=post_id
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Представление для модели Follow."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self):
        """Получение записи по фильтру."""
        return self.request.user.follower.filter(user=self.request.user)
