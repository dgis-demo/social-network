from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


from .managers import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    objects = UserManager()

    email = models.EmailField('Email address', unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        'Staff status',
        default=False,
        help_text='User cannot login without this flag'
    )

    USERNAME_FIELD = 'email'


class Post(BaseModel):
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='posts'
    )
    content = models.TextField('Content')

    def __str__(self):
        return f'{self.pk} {self.author}'


class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.pk} {self.post.author}'
