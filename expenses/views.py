"""
    Views for expense app
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/authentication/login')
def index(request):
    """Initial page

    Args:
        request (Object): Takes a request 

    Returns:
        html: Returns template for expense website landing page
        
    """
    return render(request, 'expenses/index.html')


def add_expense(request):
    """Add new expense

    Args:
        request (Object): Takes a request 

    Returns:
        html: Returns template for add expense page
        
    """
    return render(request,'expenses/add_expense.html')
