from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    fitness_goals = models.TextField(blank=True)
    current_weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    target_weight = models.FloatField(null=True, blank=True, help_text="Target weight in kg")
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        db_table = 'users'