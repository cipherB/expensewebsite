"""
    Views for expense app
"""
import os
import tempfile
import json
import csv
# import pdb
import datetime
import xlwt
from weasyprint import HTML
from django.db.models import Sum
from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
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
    currency = UserPreference.objects.get_or_create(user=request.user)[0].currency
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

def expense_category_summary(request):
    """Return a JSON object for expenses chart"""
    current_date = datetime.date.today()
    six_months_ago = current_date - datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(
        date__gte=six_months_ago,
        date__lte=current_date,
        owner=request.user
    )
    final_rep = {}
    #
    def get_category(expense):
        return expense.category
    #
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount
    #
    category_list = list(set(map(get_category, expenses)))
    for _ in expenses:
        for y in category_list:
            final_rep[y] = get_expense_category_amount(y)
    return JsonResponse({'expense_category_data': final_rep}, safe=False)

def stats_view(request):
    """Return the expense summary page"""
    return render(request, 'expenses/stats.html')

def export_csv(request):
    """Create csv file from expenses table"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+str(
        datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])
    expenses = Expense.objects.filter(owner=request.user)
    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])
    return response

def export_excel(request):
    """Create an excel file from expenses table"""
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+str(
        datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Amount', 'Description', 'Category', 'Date']
    for col_num ,label in enumerate(columns):
        ws.write(row_num, col_num, label, font_style)
    font_style = xlwt.XFStyle()
    rows = Expense.objects.filter(owner=request.user).values_list(
        'amount',
        'description',
        'category',
        'date'
    )
    for row in rows:
        row_num += 1
        for col_num, data_item in enumerate(row):
            ws.write(row_num, col_num, str(data_item), font_style)
    wb.save(response)
    return response

def export_pdf(request):
    """Create an excel file from expenses table"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Expenses'+str(
        datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    expenses = Expense.objects.filter(owner=request.user)
    sum = expenses.aggregate(Sum('amount'))
    html_string = render_to_string('expenses/pdf-output.html', 
                                   {'expenses': expenses, 'total': sum['amount__sum']})
    html = HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=False)as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response
