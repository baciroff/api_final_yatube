from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'group', 'text', 'image', 'pub_date')
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source='post.id')
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'])
        ]

    def validate(self, data):
        """Проверяем, что не подписываемся на самого себя."""
        if self.context['request'].user != data.get('following'):
            return data
        raise serializers.ValidationError("Нельзя подписаться на самого себя")
