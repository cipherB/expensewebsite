"""Import Django Libraries
"""
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class UserIncome(models.Model):
    """User Income Models

    Returns:
        creates a database model for the user income
    """
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)

    def __str__(self):
        return str(self.source)

    class Meta:
        """Meta class to sort model items by date
        """
        ordering = ['-date']
        verbose_name_plural = 'User income'

class Source(models.Model):
    """Source Model
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
