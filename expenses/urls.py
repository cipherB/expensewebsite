"""
    _summary_
    Url patterns lists all routes to the expenses app view
"""
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="expenses"),
    path('add-expense',views.add_expense, name="add-expense")
]
