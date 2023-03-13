"""Import Django libraries
"""
from django.contrib import admin
from .models import Expense, Category

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    """Modify the expense info displayed on the admin page
    """
    list_display = ('amount', 'date', 'category', 'owner', )
    list_per_page = 5

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
