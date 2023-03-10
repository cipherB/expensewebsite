"""import Django Libraries
"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPreference(models.Model):
    """User Preferences Models

    Returns:
        creates a database model for the user preferences
    """
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, default="NGN - Nigerian Naira")
    def __str__(self):
        return str(self.user)+'s'+'preferences'
