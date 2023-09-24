from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # додайте поля за вашими потребами

    def __str__(self):
        return self.username
