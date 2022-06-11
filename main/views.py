from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate, login
from .models import *
from main.MongoDbManager import MongoDbManager
from django.contrib.auth.models import User
from django.contrib.auth import login
import json
import datetime
from datetime import date, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
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
    winlog = MongoDbManager().get_winnerdb_log()._CommandCursor__data.pop()
    winupdate = MongoDbManager().get_winner_lastest()._CommandCursor__data.pop()
    sellupdate = MongoDbManager().get_seller_lastest()._CommandCursor__data.pop()
    prdupdate = MongoDbManager().get_product_lastest()._CommandCursor__data.pop()
    catlog = MongoDbManager().get_cat_log()._CommandCursor__data.pop()
    context = {
        'productdb': {'prdcount': prdcount ,  'Nprdcount': Nprdcount,'prdupdate':prdupdate['update']},
        'winnerdb': {'wincount': wincount['winner'], 'Nwincount': Nwincount['winner'],'winupdate':winupdate['update']},
        'catcount': mcatcount + wmcatcount,
        'sellerdb': {'sellcount': sellcount, 'Nsellcount' : Nsellcount,'sellupdate':sellupdate['update']},
        'winlog': winlog,
    'catlog': catlog,
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
    update = MongoDbManager().get_product_lastest()._CommandCursor__data.pop()
    show_index = ('seller_name', 'title', 'disc_price', 'ven_productcd', 'productid', 'vendorid', 'update')
    productdb =[]
    dbproduct = MongoDbManager().get_productdb_from_collection({})
    for Data in dbproduct:
        Data = {k: Data[k] for k in show_index}
        productdb.append(Data)
    datainfo =[]
    
    dbvendorDate = MongoDbManager().get_product_vendor_count()
    total_prd=0
    total_ven=0
    for Data in dbvendorDate:
        total_prd+=Data['tot_prd']
        total_ven+=Data['tot_ven']
        Data['seller_name'] = Data['_id']
        datainfo.append(Data)

    if request.method == 'GET':
        if request.GET.get('seller_name') :
            productdb = []
            dbproduct = MongoDbManager().get_productdb_from_collection({'seller_name': request.GET.get('seller_name') })
            for Data in dbproduct:
                Data = {k: Data[k] for k in show_index}
                productdb.append(Data)

            paginator = Paginator(productdb, 6000)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
            context = {
                'productdb': posts,
                'datainfo': datainfo,
                'update': update,
                'total': {'total_prd': total_prd, 'total_ven': total_ven},
                'target' : len(productdb)
            }
            return render(request, 'registration/productdb.html', context=context)
        else :
            paginator = Paginator(productdb, 6000)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
            context = {
                'productdb': posts,
                'datainfo': datainfo,
                'update': update,
                'total': {'total_prd': total_prd, 'total_ven': total_ven},
                'target' : total_ven
            }
            return render(request, 'registration/productdb.html', context=context)
    else:
        return HttpResponse(status=405)


@login_required
@csrf_exempt
def catdb(request):
    if request.method == 'POST':
        for rq in request:
            jsonObj = json.loads(rq.decode('utf-8').replace("'","\""))

        for js in jsonObj:
            MongoDbManager().remove_mancat_collection(js)

        return render(request, 'registration/catdb.html')
    else:
        context = {
        }
        return render(request, 'registration/catdb.html', context=context)

@login_required
@csrf_exempt
def womancatdb(request):
    if request.method == 'POST':
        for rq in request:
            jsonObj = json.loads(rq.decode('utf-8').replace("'", "\""))

        for js in jsonObj:
            MongoDbManager().remove_womancat_collection(js)

        return render(request, 'registration/womancatdb.html')
    else:
        context = {
        }
        return render(request, 'registration/womancatdb.html', context=context)


@login_required
def winproduct(request):
    today = datetime.date.today()
    total = MongoDbManager().get_all_winner_count()._CommandCursor__data.pop()
    update = MongoDbManager().get_winner_lastest()._CommandCursor__data.pop()
    mysellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 2})

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
            win['dif_disc_price'] = oprice - int(w['disc_price'])
            if win['delivery'] != None:
                deli = str(today.year)+"-"+win['delivery'].replace('/', '-')
                deli = datetime.datetime.strptime(deli, '%Y-%m-%d')
                dif_deli = deli-mydeli
                win['dif_deli'] = dif_deli.days


    if request.method == 'GET':
        if request.GET.get('sellername') :
            winsellect = []
            for win in winproduct :
                for w in win['winner'] :
                    if w['seller_name'] == request.GET.get('sellername') :
                        if request.GET.get('lessprice'):
                            if w['dif_disc_price'] < 0 :
                                winsellect.append(win)
                        elif request.GET.get('lessdelivery') :
                            if w['dif_deli'] < 0 :
                                winsellect.append(win)
                        else :
                            winsellect.append(win)
            paginator = Paginator(winsellect, 6000)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
            context = {
                'winproduct': posts,
                'total': total,
                'update': update,
                'winsellect' : winsellect.__len__(),
                'mysellcount' : mysellcount
            }
            return render(request, 'registration/winproduct.html', context=context)
        else:
            paginator = Paginator(winproduct,6000)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
            context = {
                'winproduct': posts,
                'total': total,
                'update': update,
                'mysellcount' : mysellcount
            }
            return render(request, 'registration/winproduct.html', context=context)

    else:
        return HttpResponse(status=405)

@login_required
def winseller(request):
    today = datetime.datetime.today()
    update = MongoDbManager().get_seller_lastest()._CommandCursor__data.pop()
    msellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 1}).count()
    mysellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 2}).count()
    csellcount = MongoDbManager().get_sellerdb_from_collection({'seller_type': 3}).count()

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
                w['vendoritemid'] = win['vendoritemid']
                if win['delivery'] != None:
                    mydeli = str(today.year) + "-" + win['delivery'].replace('/', '-')
                    mydeli = datetime.datetime.strptime(mydeli, '%Y-%m-%d')
                    win['dif_deli'] = 0
                    win['dif_price'] = 0
        for win in w['winner']:
            oprice = int(win['price'].replace(',', ''))
            win['dif_price'] = oprice - myprice
            win['dif_disc_price'] = oprice - int(w['disc_price'])
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
                    if w['dif_disc_price'] < 0:
                        less_price += 1
                    if w['delivery'] is not None:
                        deli = str(today.year) + "-" + w['delivery'].replace('/', '-')
                        deli = datetime.datetime.strptime(deli, '%Y-%m-%d')
                        dif_deli = deli - today
                        avg_deli += dif_deli.days
                    if w['dif_deli'] < 0:
                        less_deli += 1
        if mcount > 0 :
            avg_deli = round(avg_deli / mcount, 1)

        temp = {'wcount': wcount,
                'mcount': mcount,
                'less_price': less_price,
                'avg_deli': avg_deli,
                'less_deli': less_deli}

        sell.update(temp)
    if request.GET.get('sellername') :
        for sell in winseller :
            if sell['seller_name'] == request.GET.get('sellername') :
                winseller = sell
        context = {
            'winseller': winseller,
            'update': update,
            'msellcount': msellcount,
            'mysellcount': mysellcount,
            'csellcount': csellcount
        }
        return render(request, 'registration/winseller.html', context=context)
    else :
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

    sellecount = len(responseData)

    if request.method == 'GET':
        if request.GET.get('seller_type') :
            dbUserData = MongoDbManager().get_sellerdb_from_collection({'seller_type': int(request.GET.get('seller_type'))})
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
               'sellcount': sellecount,
               'Nsellcount': Nsellcount}
            return render(request, 'registration/sellerdb.html', context=context)

        elif request.GET.get('latest'):
            dbUserData = MongoDbManager().get_sellerdb_from_collection(
                {'update': {'$gt': datetime.datetime.today().strftime('%Y-%m-%d 05:00')}})
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
                       'sellcount': sellecount,
                       'Nsellcount': Nsellcount}
            return render(request, 'registration/sellerdb.html', context=context)

        else :
            context = {'sellerdb': responseData,
                   'update': update['update'],
                   'msellcount': msellcount,
                   'mysellcount': mysellcount,
                   'csellcount': csellcount,
                   'sellcount': sellecount,
                   'Nsellcount': Nsellcount}
            return render(request, 'registration/sellerdb.html', context=context)

@login_required
@permission_required('main.User',raise_exception=True)
def setting(request):
    context ={

    }
    return render(request, 'registration/setting.html', context=context)

@login_required
@permission_required('main.User',raise_exception=True)
@csrf_exempt
def seller_register(request):
    if request.method == "POST":
        form = sellerDB(request.POST)
        if form.is_valid():
            sellername = request.POST.get('sellername','')
            sellercode = request.POST.get('sellercode','')
            sellertype = request.POST.get('sellertype','')
            new_user = myseller(sellername=sellername, sellercode=sellercode, sellertype=sellertype)
            new_user.save()
            if MongoDbManager().get_sellerdb_from_collection({'seller_name': sellername}):
                MongoDbManager().update_seller({'seller_name': sellername},
                                               {'$set': {'seller_code': sellercode,
                                                'seller_type': int(sellertype),
                                                'update': datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}})
            else:
                MongoDbManager().create_new_seller({'seller_name': sellername,
                                                    'seller_code': sellercode,
                                                    'seller_type': int(sellertype),
                                                    'matching' : int(sellertype),
                                                    'total' : "0",
                                                    'total_rating' : "0",
                                                    'update': datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')})
            return redirect('sellersetting')
        else :
            for rq in request:
                jsonObj = json.loads(rq.decode('utf-8').replace("'", "\""))
            for js in jsonObj:
                MongoDbManager().update_seller(js,{'$set': { 'seller_type' :1}})
                myseller.objects.filter(sellername=js['seller_name']).update(sellertype='1')
            return render(request, 'registration/sellersetting.html')
    else:
        seller = myseller.objects.all()
        form = sellerDB()
        return render(request, 'registration/sellersetting.html', {'form': form, "seller": seller})

@login_required
@permission_required('main.User',raise_exception=True)
def setting_seller(request) :
    context = {
    }
    return render(request,'registration/seller.html', context=context)

@login_required
@permission_required('main.User',raise_exception=True)
def setting_category(request) :
    # if request.method == "POST" :

    context={
    }
    return render(request,'registration/category.html', context=context)
