from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have "is_staff" flag.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have "is_superuser" flag.')

        if not email:
            raise ValueError('An e-mail must be sent')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
