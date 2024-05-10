"""Разрешения для пользователей."""

from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Пользовательский класс для проверок."""

    def has_object_permission(self, request, view, obj):
        """Пользовательская функция для проверок."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
