from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('user', views.UserViewSet, basename='user')
router.register('post', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', views.LikesView.as_view()),
]
