from datetime import datetime

from django.db.models import Count
from django.db.models.functions import TruncDate

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView

from .models import Post, Like
from .serializers import PostSerializer, UserSerializer, LikeSerializer, UnlikeSerializer


class UserViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'})
        return Response({'status': 'error', 'message': f'{serializer.errors}'})


class PostViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'put', 'head', 'options']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['put'])
    def like(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response({'status': 'ok'})
        return Response({'status': 'error', 'message': f'{serializer.errors}'})

    @action(detail=True, methods=['put'])
    def unlike(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = UnlikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response({'status': 'ok'})
        return Response({'status': 'error', 'message': f'{serializer.errors}'})


class LikesView(APIView):
    def get(self, request):
        try:
            date_from = datetime.strptime(request.query_params.get('date_from'), '%Y-%m-%d').date()
            date_to = datetime.strptime(request.query_params.get('date_to'), '%Y-%m-%d').date()

            queryset = Like.objects.filter(
                created_at__date__range=(date_from, date_to),
            ).annotate(date=TruncDate('created_at')).values('date').annotate(likes=Count('id')).order_by('date')

            return Response({'status': 'ok', 'message': queryset})
        except (IOError, TypeError, AttributeError, ValueError, IndexError) as e:
            return Response({'status': 'error', 'message': f'{e.__class__.__name__}: {e}'})
