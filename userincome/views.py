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
from .models import Source, UserIncome
#pylint: disable=E1101
#pylint: disable=C0103
#pylint: disable=W0622

def search_incomes(request):
    """Function to Query Income search

    Args:
        request (JSON): http request

    Returns:
        list: Returns a list of values
    """
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
                amount__istartswith=search_str,
                owner=request.user
            ) | UserIncome.objects.filter(
                date__istartswith=search_str,
                owner=request.user
            ) | UserIncome.objects.filter(
                description__icontains=search_str,
                owner=request.user
            ) | UserIncome.objects.filter(
                source__icontains=search_str,
                owner=request.user
            )
        data = income.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    """Initial page 

    Args:
        request (Object): Takes a request 

    Returns:
        html: Returns template for expense website landing page
        
    """
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get_or_create(user=request.user)[0].currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


def add_income(request):
    """Add new income

    Args:
        request (Object): Takes a request 

    Returns:
        html: Returns template for add income page
        
    """
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == "GET":
        return render(request,'income/add_income.html', context)

    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request,'income/add_income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request,'income/add_income.html', context)
        UserIncome.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            source=source,
            description=description
        )
        messages.success(request, 'Record saved successfully')
        return redirect('income')

def income_edit(request, id):
    """Edit Income

    Args:
        request (JSON): Takes request
        id (int): selected income id

    Returns:
        renders edit income html page
    """
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == "GET":
        return render(request, 'income/edit-income.html', context)
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request,'income/edit-income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request,'income/edit-income.html', context)
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.save()
        messages.success(request, 'Record updated successfully')
        return redirect('income')
    else:
        messages.info(request, 'Handling post form')
        return render(request, 'income/edit-income.html',context)

def delete_income(request, id):
    """Delete Income

    Args:
        request (JSON): HTTP request
        id (int): Income primary key

    Returns:
        Redirects to Income page
    """
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Record removed')
    return redirect('income')
