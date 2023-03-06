"""
    Views for expense app
"""
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category
#pylint: disable=E1101

@login_required(login_url='/authentication/login')
def index(request):
    """Initial page

    Args:
        request (Object): Takes a request 

    Returns:
        html: Returns template for expense website landing page
        
    """
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    """Add new expense

    Args:
        request (Object): Takes a request 

    Returns:
        html: Returns template for add expense page
        
    """
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == "GET":
        return render(request,'expenses/add_expense.html', context)

    if request.method == "POST":
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request,'expenses/add_expense.html', context)
