"""Import Django Libraries
"""
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    """Expense Models

    Returns:
        creates a database model for the expenses
    """
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return str(self.category)

    class Meta:
        """Meta class to sort model items by date
        """
        ordering = ['-date']

class Category(models.Model):
    """Category Model
    """
    name = models.CharField(max_length=255)

    class Meta:
        """Change Category plural spelling in admin dashboard
        """
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.name)
