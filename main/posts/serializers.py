from rest_framework import serializers

from .models import Post, User, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'content',)


class LikeSerializer(serializers.ModelSerializer):
    is_like = serializers.BooleanField(read_only=True)
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'is_like', 'post', 'user')

    def create(self, validated_data):
        instance, _ = Like.objects.update_or_create(
            **validated_data, defaults={'is_like': True}
        )
        return instance


class UnlikeSerializer(serializers.ModelSerializer):
    is_like = serializers.BooleanField(read_only=True)
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'is_like', 'post', 'user')

    def create(self, validated_data):
        instance, _ = Like.objects.update_or_create(
            **validated_data, defaults={'is_like': False}
        )
        return instance
