from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_photo = models.ImageField("Аватар", upload_to="users/avatars/",
                                      help_text="Аватар пользователя",
                                      blank=True)
    name = models.CharField(
        max_length=100,
        verbose_name='ФИО',
        blank=True
    )

    class Meta:
        verbose_name = "Личный кабинет"
        verbose_name_plural = "Личный кабинет"

    def __str__(self):
        return self.user.username
