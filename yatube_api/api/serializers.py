"""Сериализаторы для работы с моделями приложения API."""

import base64
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Post, Group, Follow


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Сериализатор для перевода информации из одного формата в другой."""

    def to_internal_value(self, data):
        """Функция для декодирования данных."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Класс определяет метаданные для сериализатора GroupSerializer."""

        fields = ('id', 'title', 'description', 'slug')
        model = Group


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    image = Base64ImageField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        """Функция для обновления данных."""
        instance.text = validated_data.get('text', instance.text)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.image = validated_data.get('image', instance.image)
        instance.author = validated_data.get('author', instance.author)
        instance.group = validated_data.get('group', instance.group)

        instance.save()
        return instance

    class Meta:
        """Класс определяет метаданные для сериализатора CommentSerializer."""

        fields = ('id', 'text', 'pub_date', 'image', 'author', 'group')
        model = Post
        read_only_fields = ('group',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        """Класс определяет метаданные для сериализатора CommentSerializer."""

        fields = ('id', 'text', 'created', 'author', 'post')
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        """Класс определяет метаданные для сериализатора FollowSerializer."""

        fields = ('id', 'user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('following', 'user'),
                message='Нельзя подписаться еще раз на пользователя'
            )
        ]

    def validate(self, data):
        """Функция, где нельзя подписаться на самого себя."""
        if data['following'] == data['user']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data
