from django.core.checks import messages
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Expense
from django.contrib import messages
from currencypreferences.models import CurrencyPreferences

@login_required(login_url='authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    currency = CurrencyPreferences.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'currency': currency
    }
    return render(request,'expense/index.html',context)

@login_required(login_url='authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request,'expense/add_expense.html',context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        
        if not amount:
            messages.error(request,'Amount is not mentioned')
            return render(request,'expense/add_expense.html',context)
        if not description:
            messages.error(request,'Description is not mentioned')
            return render(request,'expense/add_expense.html',context)
        if not date:
            messages.error(request,'Date is not selected')
            return render(request,'expense/add_expense.html',context)
        Expense.objects.create(owner=request.user, amount=amount,date=date,description=description,category=category)
        messages.success(request,'Expenses are saved')
        return redirect('expenses')
def edit_expense(request,id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expense/edit_expense.html',context)
    if request.method == 'POST':
        
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        
        if not amount:
            messages.error(request,'Amount is not mentioned')
            return render(request,'expense/add_expense.html',context)
        if not description:
            messages.error(request,'Description is not mentioned')
            return render(request,'expense/add_expense.html',context)
        if not date:
            messages.error(request,'Date is not selected')
            return render(request,'expense/add_expense.html',context)
        expense.owner = request.user
        expense.amount=amount
        expense.date=date
        expense.description=description
        expense.category=category
        expense.save()
        messages.success(request,'Expenses updated successfully')
        return redirect('expenses')
def delete_expense(request,id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,'Expense has been deleted')
    return redirect('expenses')