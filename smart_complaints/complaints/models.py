from django.db import models
from users.models import User

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'role': 'staff'}, related_name='assigned_complaints')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"
