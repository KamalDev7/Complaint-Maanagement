from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.name} ({self.role})"
