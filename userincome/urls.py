"""
    _summary_
    Url patterns lists all routes to the user income app view
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('',views.index, name="income"),
    path('add-income',views.add_income, name="add-income"),
    path('edit-income/<int:id>',views.income_edit, name="income-edit"),
    path('delete-income/<int:id>',views.delete_income, name="income-delete"),
    path('search-incomes',csrf_exempt(views.search_incomes), name="search-incomes"),
]
