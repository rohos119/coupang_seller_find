from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import *
from main.MongoDbManager import MongoDbManager
from django.contrib.auth.models import User
from django.contrib.auth import login
import datetime
from datetime import date, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

today = datetime.datetime.today()


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/login.html', {'eroor': '아이디와 비밀번호가 일치하지 않습니다.' })
    else:
        return render(request, 'registration/login.html')
@login_required
def logout(request) :
    auth.logout(request)
    return redirect('login')

@login_required
def index(request):
    tommorrow = today+timedelta(1)
    wincount = MongoDbManager().get_all_winner_count()._CommandCursor__data.pop()
    Nwincount = MongoDbManager().get_new_winner_count()._CommandCursor__data
    if Nwincount.__len__() > 0:
        Nwincount = Nwincount.pop()
    else:
        Nwincount = {'winner': 0}
    prdcount = MongoDbManager().get_productdb_from_collection({}).count()
    sellcount = MongoDbManager().get_sellerdb_from_collection({}).count()
    Nsellcount = MongoDbManager().get_sellerdb_from_collection({'update': {'$gt': datetime.datetime.today().strftime('%Y-%m-%d 05:00')}}).count()
    mcatcount = MongoDbManager().get_all_mancat_collection({}).count()
    wmcatcount = MongoDbManager().get_all_womancat_collection({}).count()
    Nprdcount = MongoDbManager().get_productdb_from_collection({'update': {'$gt': datetime.datetime.today().strftime('%Y-%m-%d 05:00')}}).count()
    winlog = MongoDbManager().get_winnerdb_log({'end_time': {'$gt': datetime.datetime.today().strftime('%Y-%m-%d 05:00')}})

    context = {
        'productdb': {'prdcount': prdcount ,  'Nprdcount': Nprdcount},
        'winnerdb': {'wincount': wincount['winner'], 'Nwincount': Nwincount['winner']},
        'catcount': mcatcount + wmcatcount,
        'sellerdb': {'sellcount': sellcount, 'Nsellcount' : Nsellcount},
        'winlog': winlog,
        'tommorrow': {'year': tommorrow.year, 'month': tommorrow.month, 'day': tommorrow.day}
        # 'prdlog': prdlog,

    }
    return render(request, "registration/index.html", context=context)

@login_required
def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # new_user = User.objects.create_user(**form.cleaned_data)
            # new_user.save()
            if 'update' in request.POST:
                new_user = User.objects.filter(username=request.POST['username'])
                new_user['username'] = request.POST.get('username')
                new_user['password'] = request.POST['password']
                new_user['first_name'] = request.POST['first_name']
                new_user.save()
                return redirect('register')
            elif 'create' in request.POST:
                new_user = User.objects.create_user(**form.cleaned_data)
                new_user.save()
                return redirect('register')
            elif 'delete' in request.POST:
                new_user = User.objects.filter(username=request.POST.get('username'))
                new_user.delete()
                return redirect('register')
        else:
            # users = User.objects.all()
            # form = UserForm()
            # return render(request, 'registration/register.html', {'form': form})
            return redirect('register')
    else:
        users = User.objects.all()
        form = UserForm()
        return render(request, 'registration/register.html', {'form': form,"User":users})

@login_required
def productdb(request):
    # show_index = ('title', 'ven_productcd', 'productid', 'vendorid')
    # def get():
    #     dbUserData = MongoDbManager().get_productdb_from_collection({})
    #     responseData = []
    #     for Data in dbUserData[:2]:
    #         Data = {k: Data[k] for k in show_index}
    #         # 차후수정부분
    #         Data['seller_name'] = '센트럴'
    #         template_prd = loader.get_template('registration/productdb.html')
    #     return HttpResponse(template_prd.render({'responseData': responseData}, request))
    # if request.method == 'GET':
    #     return get()
    # else:
    #     return HttpResponse(status=405)
    context = {
    }
    return render(request, 'registration/productdb.html', context=context)


@login_required
def catdb(request):
    context = {
    }
    return render(request, 'registration/catdb.html', context=context)

@login_required
def womancatdb(request):
    context = {
    }
    return render(request, 'registration/womancatdb.html', context=context)


@login_required
def winproduct(request):
    today = datetime.date.today()
    winproduct = []
    dbwinnerDate = MongoDbManager().get_winnerdb_from_collection({})
    for Data in dbwinnerDate:
        target = Data['winner']
        Data['winner'] = sorted(target, key=lambda target: target['price'])
        winproduct.append(Data)

    for w in winproduct:
        for win in w['winner']:
            if w['seller_name'] == win['seller_name']:
                w['myprice'] = win['price']
                myprice = int(win['price'].replace(',', ''))
                w['mydelievery'] = win['delivery']
                if win['delivery'] != None:
                    mydeli = str(today.year)+"-"+win['delivery'].replace('/', '-')
                    mydeli = datetime.datetime.strptime(mydeli, '%Y-%m-%d')
        for win in w['winner']:
            oprice = int(win['price'].replace(',', ''))
            win['dif_price'] = oprice - myprice
            if win['delivery'] != None:
                deli = str(today.year)+"-"+win['delivery'].replace('/', '-')
                deli = datetime.datetime.strptime(deli, '%Y-%m-%d')
                dif_deli = deli-mydeli
                win['dif_deli'] = dif_deli.days

    total = len(winproduct)
    update = MongoDbManager().get_winner_lastest()._CommandCursor__data.pop()
    if request.method == 'GET':
        context = {
            'winproduct': winproduct,
            'total': total,
            'update': update
        }
        return render(request, 'registration/winproduct.html', context=context)
    else:
        return HttpResponse(status=405)

@login_required
def winseller(request):
    today = datetime.datetime.today()
    winproduct = []
    dbwinnerDate = MongoDbManager().get_winnerdb_from_collection({})
    for Data in dbwinnerDate:
        target = Data['winner']
        Data['winner'] = sorted(target, key=lambda target: target['price'])
        winproduct.append(Data)

    for w in winproduct:
        for win in w['winner']:
            if w['seller_name'] == win['seller_name']:
                w['myprice'] = win['price']
                myprice = int(win['price'].replace(',', ''))
                w['mydelievery'] = win['delivery']
                if win['delivery'] != None:
                    mydeli = str(today.year) + "-" + win['delivery'].replace('/', '-')
                    mydeli = datetime.datetime.strptime(mydeli, '%Y-%m-%d')
        for win in w['winner']:
            oprice = int(win['price'].replace(',', ''))
            win['dif_price'] = oprice - myprice
            if win['delivery'] != None:
                deli = str(today.year) + "-" + win['delivery'].replace('/', '-')
                deli = datetime.datetime.strptime(deli, '%Y-%m-%d')
                dif_deli = deli - mydeli
                win['dif_deli'] = dif_deli.days

    winseller =[]
    dbwinseller = MongoDbManager().get_sellerdb_from_collection({})
    for Data in dbwinseller:
        winseller.append(Data)
    myseller =[]
    for sell in winseller:
        wcount = 0
        mcount = 0
        avg_deli = 0
        less_deli = 0
        less_price = 0
        for win in winproduct:
            if sell['seller_name'] == win['winner'][0]['seller_name']:
                wcount += 1
            for w in win['winner']:
                if sell['seller_name'] == w['seller_name']:
                    mcount += 1
                    if w['dif_price'] < 0:
                        less_price += 1
                    if w['delivery'] is not None:
                        deli = str(today.year) + "-" + w['delivery'].replace('/', '-')
                        deli = datetime.datetime.strptime(deli, '%Y-%m-%d')
                        dif_deli = deli - today
                        avg_deli += dif_deli.days
                        if w['dif_deli'] < 0:
                            less_deli += 1
        temp = {'wcount': wcount,
                'mcount': mcount,
                'less_price': less_price,
                'avg_deli': round(avg_deli / mcount, 1),
                'less_deli': less_deli}

        sell.update(temp)
    update = MongoDbManager().get_seller_lastest()._CommandCursor__data.pop()
    msellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 1}).count()
    mysellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 2}).count()
    csellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 3}).count()
    context = {
        'winseller': winseller,
        'update': update,
        'msellcount': msellcount,
        'mysellcount': mysellcount,
        'csellcount': csellcount

    }
    return render(request, 'registration/winseller.html', context=context)

@login_required
def sellerdb(request):
    # msellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 1, 'update': {'$gt': datetime.datetime.today().strftime('%Y-%m-%d 05:00')}}).count()
    # mysellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 2, 'update': {'$gt': datetime.datetime.today().strftime('%Y-%m-%d 05:00')}}).count()
    # csellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 3, 'update': {'$gt': datetime.datetime.today().strftime('%Y-%m-%d 05:00')}}).count()
    msellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 1}).count()
    mysellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 2}).count()
    csellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 3}).count()
    update = MongoDbManager().get_seller_lastest()._CommandCursor__data.pop()
    Nsellcount = MongoDbManager().get_sellerdb_from_collection(
        {'update': {'$gt': datetime.datetime.today().strftime('%Y-%m-%d 05:00')}}).count()
    dbUserData = MongoDbManager().get_sellerdb_from_collection({})
    responseData = []
    for Data in dbUserData:
        # Data = {k: Data[k] for k in show_index}
        # 차후수정부분
        # Data['seller_name'] = '센트럴'
        responseData.append(Data)

    context = {'sellerdb': responseData,
               'update': update['update'],
               'msellcount': msellcount,
               'mysellcount': mysellcount,
               'csellcount': csellcount,
               'sellcount': len(responseData),
               'Nsellcount': Nsellcount}

    return render(request, 'registration/sellerdb.html', context=context)

@login_required
def setting(request):
    context ={

    }
    return render(request, 'registration/setting.html', context=context)

@login_required
def seller_register(request):
    if request.method == "POST":
        form = sellerDB(request.POST)
        if form.is_valid():
            sellername = request.POST.get('sellername','')
            sellercode = request.POST.get('sellercode','')
            sellertype = request.POST.get('sellertype','')
            new_user = myseller(sellername=sellername, sellercode=sellercode, sellertype=sellertype)
            new_user.save()
            # return redirect("http://127.0.0.1:8000/login/setting/register")
            return redirect('sellersetting')
    else:
        seller = myseller.objects.all()
        form = sellerDB()
        return render(request, 'registration/sellersetting.html', {'form': form, "seller": seller})

@login_required
def setting_seller(request) :
    context = {
    }
    return render(request,'registration/seller.html', context=context)

@login_required
def setting_category(request) :
    # if request.method == "POST" :

    context={
    }
    return render(request,'registration/category.html', context=context)
