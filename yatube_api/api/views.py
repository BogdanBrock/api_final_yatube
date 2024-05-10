"""Представления для работы с моделями приложения API."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
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
        group_id_str = self.request.data.get('group')
        group_id_int = int(group_id_str) if group_id_str else None
        serializer.save(author=self.request.user, group_id=group_id_int)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [
        IsOwnerOrReadOnly
    ]


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        """Получение записи авторизированным пользователем."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.filter(post_id=post_id)

    def perform_create(self, serializer):
        """Создание записи без указания номера поста и автора в запросе."""
        post_id = self.kwargs.get('post_id')
        get_object_or_404(Post, id=post_id)
        serializer.save(
            author_id=self.request.user.id,
            post_id=post_id
        )


class FollowViewSet(viewsets.ModelViewSet):
    """Представление для модели Follow."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ("user__username", "following__username")

    def get_queryset(self):
        """Получение записи по фильтру."""
        user = get_object_or_404(User, username=self.request.user)
        return Follow.objects.filter(user=user)
