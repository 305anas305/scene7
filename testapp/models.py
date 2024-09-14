from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, first_name=None, last_name=None):
        if not username:
            raise ValueError('The Username field is required')
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, first_name=None, last_name=None):
        user = self.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username
class blog(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
