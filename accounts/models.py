from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    gender = models.CharField(max_length=1)
    contact = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    name = models.CharField(max_length=20)


class Book(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    information = models.CharField(max_length=200)
