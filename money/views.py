from django.shortcuts import render
from .models import Banks,Transactions, User
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import jdatetime
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
# from django.contrib.auth.models import User


@login_required(login_url=r'accounts/login')
def index(requset,type):
    context = {}
    sum = 0
    selectedSource = None

    if int(type) == 1:
        context['listTitle'] = "درآمد ها"
    elif int(type) == 2:
        context['listTitle'] = 'هزینه ها'
    elif int(type) == 3:
        context['listTitle'] = 'حساب ها'
    elif int(type) == 4:
        context['listTitle'] = 'بدهی ها'
    elif int(type) == 5:
        context['listTitle'] = 'مطالبه ها'

    # this two lines use for get all bank name and show them in html
    source = Banks.objects.all().filter(owner=requset.user)
    context['name_bank'] = source

    # this if condition use for get type and bank selected by use for filtering
    if requset.method == 'POST':
        selectedSource = int(requset.POST.get("bank",0))

    if selectedSource is not None and selectedSource != 0:
        transactions = Transactions.objects.filter(type=type, source=selectedSource,owner=requset.user)
        sourcName = Banks.objects.get(id=selectedSource)
        context['selected_source'] = sourcName
        context['transactions'] = transactions
    else:
        transactions = Transactions.objects.filter(type=type,owner=requset.user)
        context['transactions'] = transactions

    # this loop calculate sum of transactions just in one type
    for transaction in transactions:
        cash = transaction.cash
        sum = cash + sum
    context['sumOfType'] = sum

    # this lines use for get sum of income end cash in bank and radius that from sum of expense
    sumOfIncome = 0
    sumOfExpens = 0

    # this two lines use for get all of the expenses and incomes
    incomes = Transactions.objects.filter(type=1,source=selectedSource,owner=requset.user.id)
    expenses = Transactions.objects.filter(type=2,source=selectedSource,owner=requset.user.id)

    # this if check the source is selected or not, if it is selected the value of that is not equal to 0
    if selectedSource is not None and selectedSource != 0:
        cashOfBank = Banks.objects.filter(id=selectedSource,owner=requset.user.id)
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

    if requset.method == 'POST':
        idForChage = requset.POST.get("change")
        if idForChage is not None:
            return HttpResponseRedirect(reverse('change', kwargs={'id': idForChage}))



    context['user'] = requset.user
    return render(requset,'money/transactions.html',context)


@login_required(login_url=r'accounts/login')
def changeTransaction(request,id):

    context = {}

    all = Transactions.objects.filter(id=id)
    for transactions in all:
        context['title'] = transactions.title
        context['cash'] = transactions.cash
        context['bank'] = transactions.source
        context['desc'] = transactions.desc

    # this two lines use for get name of banks and show them in html
    source = Banks.objects.all().values('name_bank').filter(owner=request.user)
    context['banks'] = source

    if 'update' in request.POST:
        title = request.POST.get("title")
        if title == "":
            context["saveTransaction"] = 2

        cash = request.POST.get("cash")
        if cash == "":
            context["saveTransaction"] = 3

        desc = request.POST.get("desc")
        if desc == "":
            desc = "بدون توضیحات"

        bank = Banks.objects.get(name_bank=request.POST.get("bank"))
        try:
            Transactions.objects.filter(id=id).update(title=title, cash=cash, desc=desc, source=bank)
            context["saveTransaction"] = 4
            messages.error(request, 'تراکنش شما به موفقیت به روز رسانی شد')
        except:
            print("cont update transaction")

    elif 'delete' in request.POST:
        typeList = Transactions.objects.filter(id=id)
        type = 0
        for typeLists in typeList:
            type = typeLists.type
        Transactions.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse('transactions', kwargs={'type': type}))


    return render(request, 'money/changeTransaction.html', context)


@login_required(login_url=r'accounts/login')
def addTransaction(request, type):
    context = {}

    # this two lines use for get name of banks and show them in html
    source = Banks.objects.all().values('name_bank').filter(owner=request.user)
    context['name_bank'] = source


    if int(type) == 1:
        context['listTitle'] = "درآمد"
    elif int(type) == 2:
        context['listTitle'] = 'هزینه'
    elif int(type) == 3:
        context['listTitle'] = 'حساب'
    elif int(type) == 4:
        context['listTitle'] = 'بدهی'
    elif int(type) == 5:
        context['listTitle'] = 'مطالبه'

    # type_transaction = request.session.get('selected_type')
    type_transaction = type
    if request.method == 'POST':
        try:
            # theses lines use for get values from html
            title = request.POST.get("title")
            if title == "":
                context["saveTransaction"] = 2

            cash = request.POST.get("cash")
            if cash == "":
                context["saveTransaction"] = 3
                print("cash is: ", cash)

            desc = request.POST.get("desc")
            if desc == "":
                desc = "بدون توضیحات"
            bank = Banks.objects.get(name_bank=request.POST.get("bank"))
            date = request.POST.get("date")

            date = stringToDate(date)

            # this line use for save data in database
            Transactions(source=bank, date=date, title=title, cash=cash, desc=desc, type=type_transaction, owner=request.user).save()

            selectedBank = Banks.objects.filter(name_bank=bank)

            for selectedBanks in selectedBank:
                cashInBnak = selectedBanks.cash_bank

            cashInBnak = int(cashInBnak)
            cash = int(cash)

            if int(type) == 1:
                updateCash = cash + cashInBnak
                Banks.objects.filter(name_bank=bank).update(cash_bank=updateCash)
                print("cash is:", cash)
                print("cash in bank is:", cashInBnak)
                print("updated cash for income is:", updateCash)
            elif int(type) == 2:
                updateCash = cashInBnak - cash
                Banks.objects.filter(name_bank=bank).update(cash_bank=updateCash)
                print("cash is:", cash)
                print("cash in bank is:", cashInBnak)
                print("updated cash for cost is:", updateCash)

            context["saveTransaction"] = 4
        except:
            pass


    context['user'] = request.user
    return render(request, 'money/AddPage.html',context)


@login_required(login_url=r'accounts/login')
def addBank(request, type):
    context = {}

    # first if check the name of bank is null or not if it was null we have an error print
    if request.method == 'POST':
        # this two lines get name and cash of bank for save in db
        nameOfBank = request.POST.get("bankName")
        cashOfBank = request.POST.get("cashInBank")

        if nameOfBank is None or nameOfBank == "":
            context["saveBank"] = 0
            messages.error(request, 'نام حساب را به درستی وارد کنید')
        else:
            # this if check the cash is null or not, if it was null we assign 0 to cash_bank
            if cashOfBank is None or cashOfBank == '':
                cashOfBank = 0
                Banks(name_bank=nameOfBank,cash_bank= cashOfBank,owner=request.user).save()
                context["saveBank"] = 1
                messages.error(request, 'حساب شما با موفقیت ذخیره شد')
            else:
                Banks(name_bank=nameOfBank, cash_bank=cashOfBank,owner=request.user).save()
                context["saveBank"] = 1
                messages.error(request, 'حساب شما با موفقیت ذخیره شد')



    context['user'] = request.user
    return render (request, 'money/addBank.html',context)


@login_required(login_url=r'accounts/login')
def banks(request,type):
    context = {}
    allbanks = Banks.objects.all().filter(owner=request.user)
    sumOfBnak = 0
    for allbank in allbanks:
        cashInBank = allbank.cash_bank
        sumOfBnak = cashInBank + sumOfBnak
    context['sum_cash_bank'] = sumOfBnak
    context['all_banks'] = allbanks
    context['user'] = request.user

    return render(request,'money/banks.html', context)


def changeBank(request,id):
    context = {}

    bank = Banks.objects.filter(id=id)
    for bankDetail in bank:
        context['bankName'] = bankDetail.name_bank
        context['bankCash'] = bankDetail.cash_bank

    if 'update' in request.POST:
        # this two lines get name and cash of bank for save in db
        nameOfBank = request.POST.get("bankName")
        cashOfBank = request.POST.get("cashInBank")

        if nameOfBank is None or nameOfBank == "":
            context["saveBank"] = 0
            messages.error(request, 'نام حساب را به درستی وارد کنید')
        else:
            # this if check the cash is null or not, if it was null we assign 0 to cash_bank
            if cashOfBank is None or cashOfBank == '':
                cashOfBank = 0
                Banks.objects.filter(id=id).update(name_bank=nameOfBank, cash_bank=cashOfBank)
                context["saveBank"] = 1
                messages.error(request, 'حساب شما با موفقیت به روز رسانی شد')
                return HttpResponseRedirect(reverse('banks', kwargs={'type': 3}))
            else:
                Banks.objects.filter(id=id).update(name_bank=nameOfBank, cash_bank=cashOfBank)
                context["saveBank"] = 1
                messages.error(request, 'حساب شما با موفقیت به روز رسانی شد')
                return HttpResponseRedirect(reverse('banks', kwargs={'type': 3}))
    elif 'delete' in request.POST:
        Banks.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse('banks', kwargs={'type': 3}))


    return render(request,'money/changeBank.html', context)

def clogin(request):
    context = {}
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.GET.get("next", "/"))
        print("user is_authenticated ")
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = authenticate(username=username,password=password)
        except:
            user = None
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(request.GET.get("get","/money"))
            else:
                print("The Username Or Password is incorrect!")
    return render(request, 'money/login.html', context)


@login_required
def clogout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(request.GET.get("next","/money"))


def register(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get("firstName")
        emailAddress = request.POST.get("emailAddress")
        password = request.POST.get("password")

        if username is not None:
            if User.objects.filter(username=username).exists():
                context['success'] = 1
                messages.error(request, 'شما از قبل ثبت نام نموده اید')
            else:
                user = User.objects.create_user(username, emailAddress, password)
                user.save()
                context['success'] = 2
                messages.error(request, 'ثبت نام شما با موفقیت انجام شد')
                return HttpResponseRedirect(reverse('login'), context)

    return render(request, 'money/register.html',context)


@login_required(login_url=r'accounts/login')
def homePage(requset):
    context = {}

    user =  User.objects.filter(username=requset.user)
    for users in user:
        if users.firstLoad == True:
            context['firstLoad'] = True
            User.objects.filter(username=requset.user).update(firstLoad=False)
        else:
            context['firstLoad'] = False

    if requset.method == 'POST':
        typeAdd = requset.POST.get("add")
        if typeAdd == "1" or typeAdd == "2" or typeAdd == "4" or typeAdd == "5":
            # requset.session['selected_type'] = typeAdd
            typeAdd = int(typeAdd)
            return HttpResponseRedirect(reverse('addTransactions', kwargs={'type':typeAdd}))
        if typeAdd == "3":
            # requset.session['selected_type'] = typeAdd
            typeAdd = int(typeAdd)
            return HttpResponseRedirect(reverse('addBank', kwargs={'type':typeAdd}))


        typeList = requset.POST.get("list")
        if typeList == "1" or typeList == "2" or typeList == "4" or typeList == "5":
            # requset.session['selected_type_list'] = typeList
            return HttpResponseRedirect(reverse('transactions', kwargs={'type':typeList}))
        if typeList == "3":
            # requset.session['selected_type_list'] = typeList
            return HttpResponseRedirect(reverse('banks', kwargs={'type':typeList}))
        if typeList == "0":
            return HttpResponseRedirect(reverse('report'))



    return render(requset,'money/home.html',context)

def report(requset):
    context = {}
    selectedSource = None
    allIncome = []
    allExpense = []
    allTransaction = []
    income = 0
    expense = 0

    # this two lines use for get all bank name and show them in html
    source = Banks.objects.all().filter(owner=requset.user)
    context['bank'] = source

    # # this two lines use for get today month and today year
    monthNumber = jdatetime.date.today().month
    yearNumber = jdatetime.date.today().year

    # this two lines calculate start and end of month
    startDayOfMonth = jdatetime.datetime(yearNumber,monthNumber,1)
    endDayOfMonth = jdatetime.datetime(yearNumber,monthNumber + 1,1,00,00,00)

    # this two lines convert persian date to gregorian date and time
    startDayOfMonthGregorianDateTime = startDayOfMonth.togregorian()
    endDayOfMonthGregorianDateTime = endDayOfMonth.togregorian()

    # this two lines convert date time to date
    startDayOfMonthGregorianDate = datetime.date(startDayOfMonthGregorianDateTime)
    endDayOfMonthGregorianDate = datetime.date(endDayOfMonthGregorianDateTime)


    context['start_date'] = startDayOfMonth
    context['end_date'] = endDayOfMonth
    # except:
    if requset.method == 'POST':
        # the two below lines use for get selected date from user
        startDayFilter = requset.POST.get("start_date", None)
        endDayFilter = requset.POST.get("end_date", None)

        # the two below lines use for set selected date after submit and show it to user
        context['start_date'] = startDayFilter
        context['end_date'] = endDayFilter

        startDayOfMonthGregorianDate = stringToDate(startDayFilter)
        endDayOfMonthGregorianDate = stringToDate(endDayFilter)

        selectedSource = int(requset.POST.get("bank", 0))


    if selectedSource is not None and selectedSource != 0:
        transaction = Transactions.objects.filter(owner=requset.user, source=selectedSource,date__range=[startDayOfMonthGregorianDate,endDayOfMonthGregorianDate])
        bankNamme = Banks.objects.filter(id=selectedSource)
        for bankNammes in bankNamme:
            context['selected_source'] = bankNammes.name_bank
    else:
        # the below line use for get all transactions by that user is log in
        transaction = Transactions.objects.all().filter(owner=requset.user, date__range=[startDayOfMonthGregorianDate,endDayOfMonthGregorianDate])

    # the below loop use for separate the incomes and costs from all transactions and put them in separate arrays
    for transactions in transaction:
        if transactions.type == 1:
            allIncome.append(transactions)
        if transactions.type == 2:
            allExpense.append(transactions)


    # the two below loops use for calculate sum of incomes and costs
    for incomes in allIncome:
        income = income + incomes.cash

    for expenses in allExpense:
        expense = expense + expenses.cash

    for allTransactions in transaction:
        if allTransactions.type == 1 or allTransactions.type == 2:
            allTransaction.append(allTransactions)

    context['reportArray'] = allTransaction

    sum = income - expense
    context['sum'] = sum

    return render(requset,'money/report.html', context)

def getDataChart(request):
    allbank = Banks.objects.all().filter(owner=request.user)
    labels = []
    defaultItmes = []
    for allbanks in allbank:
        labels.append(allbanks.name_bank)
        defaultItmes.append(allbanks.cash_bank)
    date = {
        "labels": labels,
        "default": defaultItmes,
    }
    return JsonResponse(date)

# this function use for convert an array of string to gregorian
def stringToDate(string):
    # this tree line use for convert persian date to gregorian
    string.split('/')
    firstY = string[0]
    seconY = string[1]
    thirdY = string[2]
    forthY = string[3]
    firstM = string[5]
    seconM = string[6]
    firstD = string[8]
    seconD = string[9]
    yearString = firstY + seconY + thirdY + forthY
    monthString = firstM + seconM
    dayString = firstD + seconD

    date = jdatetime.date(int(yearString), int(monthString), int(dayString), locale='fa_IR')
    date = date.togregorian()
    return date