from django.shortcuts import render
from django.http import HttpResponse
from .models import Banks,Transactions
from django.contrib.auth import authenticate,login,logout
from django.http.response import HttpResponseRedirect


def index(requset):
    context = {}
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

    # this lines use for get sum of income end cash in bank and radius that from sum of expense
    sumOfIncome = 0
    sumOfExpens = 0

    # this two lines use for get all of the expenses and incomes
    incomes = Transactions.objects.filter(type=1,source=selectedSource)
    expenses = Transactions.objects.filter(type=2,source=selectedSource)

    # this if check the source is selected or not, if it is selected the value of that is not equal to 0
    if selectedSource is not None and selectedSource != 0:
        cashOfBank = Banks.objects.filter(id=selectedSource)
        for cashOfBanks in cashOfBank:
            cashOfSelectedBank = cashOfBanks.cash_bank
        for income in incomes:
            cashOfIncome = income.cash
            sumOfIncome = sumOfIncome + cashOfIncome
        for expense in expenses:
            cashOfExpense = expense.cash
            sumOfExpens = sumOfExpens + cashOfExpense
        sumOfBank = (sumOfIncome + cashOfSelectedBank) - sumOfExpens
        context['sum_bank'] = sumOfBank
    else:
        cashOfSelectedBank = 0
        for income in incomes:
            cashOfIncome = income.cash
            sumOfIncome = sumOfIncome + cashOfIncome
        for expense in expenses:
            cashOfExpense = expense.cash
            sumOfExpens = sumOfExpens + cashOfExpense
        sumOfBank = (sumOfIncome + cashOfSelectedBank) - sumOfExpens
        context['sum_bank'] = sumOfBank

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


def addBank(request):
    context = {}

    # this two lines get name and cash of bank for save in db
    nameOfBank = request.POST.get("bankName")
    cashOfBank = request.POST.get("cashInBank")

    # first if check the name of bank is null or not if it was null we have an error print
    if nameOfBank is None or nameOfBank == '':
        print("please enter a name for bank")
    else:
        # this if check the cash is null or not, if it was null we assign 0 to cash_bank
        if cashOfBank is None or cashOfBank == '':
            cashOfBank = 0
            Banks(name_bank=nameOfBank,cash_bank= cashOfBank).save()
            print("save company successfully and cash in it is:", cashOfBank)
        else:
            Banks(name_bank=nameOfBank, cash_bank=cashOfBank).save()
            print("save company successfully and cash in it is:", cashOfBank)

    return render (request, 'money/addBank.html',context)


def banks(request):
    context = {}
    allbanks = Banks.objects.all()
    sumOfBnak = 0
    for allbank in allbanks:
        cashInBank = allbank.cash_bank
        sumOfBnak = cashInBank + sumOfBnak
    context['sum_cash_bank'] = sumOfBnak
    context['all_banks'] = allbanks
    return render(request,'money/banks.html', context)


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