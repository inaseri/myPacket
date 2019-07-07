from django.shortcuts import render
from django.http import HttpResponse
from .models import Banks,Transactions
from django.contrib.auth import authenticate,login,logout
from django.http.response import HttpResponseRedirect


def index(requset):
    context = {}
    type = 1
    sum = 0
    selectedSource = None

    # this two lines use for get all bank name and show them in html
    source = Banks.objects.all()
    context['name_bank'] = source

    # this if condition use for get type and bank selected by use for filtering
    if requset.method == 'POST':
        selectedSource = int(requset.POST.get("bank",0))

    if selectedSource is not None and selectedSource != 0:
        type = requset.POST.get("income")
        if type is None:
            type = 1
        transactions = Transactions.objects.filter(type=type, source=selectedSource)
        sourcName = Banks.objects.get(id=selectedSource)
        context['selected_source'] = sourcName
        context['transactions'] = transactions
    else:
        type = requset.POST.get("income")
        if type is None:
            type = 1
        transactions = Transactions.objects.filter(type=type)
        context['transactions'] = transactions

    # this four conditions use for check for type
    if int(type) == 1:
        context['type'] = "درآمد"
        context['type_int'] = 1
    elif int(type) == 2:
        context['type'] = "هزینه"
        context['type_int'] = 2
    elif int(type) == 3:
        context['type'] = "بدهی"
        context['type_int'] = 3
    else:
        context['type'] = "مطالبه"
        context['type_int'] = 4

    # this loop calculate sum of transactions just in one type
    for transaction in transactions:
        cash = transaction.cash
        sum = cash + sum
    context['sumOfType'] = sum

    # this lines use for get sum of income end radius that from sum of expense
    sumOfIncome = 0
    sumOfExpens = 0
    incomes = Transactions.objects.filter(type=1)
    expenses = Transactions.objects.filter(type=2)
    for income in incomes:
        cashOfIncome = income.cash
        sumOfIncome = sumOfIncome + cashOfIncome
    for expense in expenses:
        cashOfExpense = expense.cash
        sumOfExpens = sumOfExpens + cashOfExpense
    sumOfBank = sumOfIncome - sumOfExpens

    return render(requset,'money/transactions.html',context)


def addTransaction(request):
    context = {}

    # this two lines use for get name of banks and show them in html
    source = Banks.objects.all().values('name_bank')
    context['name_bank'] = source

    if request.method == 'POST':
        try:
            # theses lines use for get values from html
            type_transaction = request.POST.get("income")
            bank = Banks.objects.get(name_bank=request.POST.get("bank"))
            date = request.POST.get("date")
            title = request.POST.get("title")
            cash = request.POST.get("cash")
            desc = request.POST.get("desc")

            # this line use for save data in database
            Transactions(source=bank, date=date, title=title, cash=cash, desc=desc, type=type_transaction).save()
            print("saved")
        except:
            pass

    return render(request, 'money/addPage.html',context)


def cLogin(request):
    context = {}
    username = 'iman'
    password = '3802'
    user = authenticate(request, username=username, password=password)
    print("user is:",user)
    if user is not None:
        login(request, user)
        return render(request,'money/transactions.html')
        print("login is success fully")
    else:
        return HttpResponseRedirect('money/login.html')
    return render(request, 'money/login.html', context)

