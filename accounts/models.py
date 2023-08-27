import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager
from accounts.validators import validate_username, validate_name, validate_birth_date


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, validators=[validate_username])
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50, validators=[validate_name])
    last_name = models.CharField(max_length=50, validators=[validate_name])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.username = self.username.lower()
        super().save(*args, **kwargs)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='profile')
    avatar = models.URLField(max_length=255, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    bio = models.TextField()
    info = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return f'Profile\'s of user {self.user.username}'

    def create_avatar(self):
        md5_hash = hashlib.md5(self.user.email.lower().encode('utf-8')).hexdigest()
        gravatar_url = f'https://www.gravatar.com/avatar/{md5_hash}?d=identicon&s={200}'
        self.avatar = gravatar_url

    def subscribe(self, user) -> bool:
        return ProfileSubscription.objects.filter(profile=self, user=user).exists()

    def unsubscribe(self, user):
        ProfileSubscription.objects.filter(user=user, profile=self).exists()

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        if not self.avatar:
            self.create_avatar()
        super().save(*args, **kwargs)


class ProfileSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscription')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscription')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'profile')

    def __str__(self):
        return f'{self.user} - {self.profile}'
