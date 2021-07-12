from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', TemplateView.as_view(template_name='swagger.html')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
    path('login/', TokenObtainPairView.as_view()),
]
