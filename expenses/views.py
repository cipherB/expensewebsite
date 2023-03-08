"""
    Views for expense app
"""
import json
# import pdb
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from userpreferences.models import UserPreference
from .models import Category, Expense
#pylint: disable=E1101
#pylint: disable=C0103
#pylint: disable=W0622

def search_expenses(request):
    """Function to Query Expense search

    Args:
        request (JSON): http request
        
    Returns:
        list: Returns a list of values
    """
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
                amount__istartswith=search_str,
                owner=request.user
            ) | Expense.objects.filter(
                date__istartswith=search_str,
                owner=request.user
            ) | Expense.objects.filter(
                description__icontains=search_str,
                owner=request.user
            ) | Expense.objects.filter(
                category__icontains=search_str,
                owner=request.user
            )
        data = expenses.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    """Initial page 

    Args:
        request (Object): Takes a request 

    Returns:
        html: Returns template for expense website landing page
        
    """
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
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
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request,'expenses/add_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request,'expenses/add_expense.html', context)
        Expense.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            category=category,
            description=description
        )
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')

def expense_edit(request, id):
    """Edit Expenses

    Args:
        request (JSON): Takes request
        id (int): selected expense id

    Returns:
        renders edit expense html page
    """
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == "GET":
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request,'expenses/edit-expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request,'expenses/edit-expense.html', context)
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()
        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')
    else:
        messages.info(request, 'Handling post form')
        return render(request, 'expenses/edit-expense.html',context)

def delete_expense(request, id):
    """Delete Expense

    Args:
        request (JSON): HTTP request
        id (int): Expense primary key

    Returns:
        Redirects to Expense page
    """
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')
