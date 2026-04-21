from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.username})


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Профіль {self.user.username}'

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/img/default_avatar.png'
