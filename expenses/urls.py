"""
    _summary_
    Url patterns lists all routes to the expenses app view
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('',views.index, name="expenses"),
    path('add-expense',views.add_expense, name="add-expense"),
    path('edit-expense/<int:id>',views.expense_edit, name="expense-edit"),
    path('delete-expense/<int:id>',views.delete_expense, name="expense-delete"),
    path('search-expenses',csrf_exempt(views.search_expenses), name="search-expenses"),
]
