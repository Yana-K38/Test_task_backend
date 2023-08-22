from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is None:
            extra_fields['is_staff'] = False
        if extra_fields.get('is_superuser') is None:
            extra_fields['is_superuser'] = False

        if not email:
            raise ValueError('The Email field must be set')
        
        username = email  # Set email as username
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    objects = CustomUserManager()
    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        
    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_photo = models.ImageField("Аватар", upload_to="app/avatars/",
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
