from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core import validators

class UserManager(BaseUserManager):
    def create_user(self, **fields):
        if not 'email' in fields:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(fields['email'])
        user = self.model(email=fields['email'], nickname=fields['nickname'])
        user.set_password(fields['password'])
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = models.CharField(max_length=10)
    nickname= models.CharField(max_length=15)
    email = models.EmailField(unique=True, validators=[validators.EmailValidator],)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    first_name, last_name = None, None
    
    fcm_token = models.CharField(null=True, max_length=200)

    objects = UserManager()
    
class EmailCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_code')