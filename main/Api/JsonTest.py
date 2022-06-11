from django.http import HttpResponse
import json
import datetime
from bson import ObjectId
from main.MongoDbManager import MongoDbManager

#
# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)
#
# def json_default(value):
#     if isinstance(value, datetime.date):
#         return value.strftime('%Y-%m-%d')
#     raise TypeError('not JSON serializable')
#     data = {'date': datetime.date.today()}
#     json_data = json.dumps(data, default=json_default)



def all_sellerdb(request):
    # show_index = ('seller_name','seller_number', 'update')
    def get():
        dbUserData = MongoDbManager().get_sellerdb_noduplicate_from_collection()
        responseData = []
        for Data in dbUserData:
            # Data = {k: Data[k] for k in show_index}
            # 차후수정부분
            # Data['seller_name'] = '센트럴'
            responseData.append(Data)
        return HttpResponse(json.dumps(responseData), status=200)

    if request.method == 'GET':
        return get()
    else:
        return HttpResponse(status=405)


def all_productdb(request):
    show_index =('seller_name','title','disc_price','ven_productcd','productid','vendorid','update')
    def get():
        #productData 추출
        dbproductData = MongoDbManager().get_productdb_from_collection({})
        responseData = []
        for Data in dbproductData[:100]:
            Data = {k:Data[k] for k in show_index}
            #차후수정부분
            responseData.append(Data)

        #product 셀러별 추출
        pipeline = [
        {
            '$group': {
                '_id': {
                    'seller_name': '$seller_name',
                    'productid': '$productid'
                },
                'c_ven': {
                    '$sum': 1
                }
            }
        },
        {
            '$group': {
                '_id': '$_id.seller_name',
                'tot_prd': {
                    '$sum': 1
                },
                'tot_ven': {
                    '$sum': '$c_ven'
                }
            }
        }
        ]
        datainfo=[]
        dbvendorDate = MongoDbManager().get_product_vendor_count()
        for Data in dbvendorDate:
            datainfo.append(Data)
        responseData.append(datainfo)
        return HttpResponse(json.dumps(responseData), status=200)
    if request.method == 'GET':
        return get()
    else:
        return HttpResponse(status=405)

# def delete_productdb(request):
#     if request.method =="POST":
#         return HttpResponse(json.load(response))
#

def man_category(request) :
    show_index = ('catname', 'catnum', 'update','crawl_update')
    def get():
        dbUserData = MongoDbManager().get_all_mancat_collection({})
        responseData = []
        for Data in dbUserData:
            Data = {k: Data[k] for k in show_index}
            # 차후수정부분
            responseData.append(Data)
        setting =[]
        settings=MongoDbManager().get_setcat({})
        for set in settings:
            setting.append(set)
        responseData.append(setting)
        return HttpResponse(json.dumps(responseData), status=200)

    if request.method == 'GET':
        return get()
    else:
        return HttpResponse(status=405)

def woman_category(request) :
    show_index = ('catname', 'catnum', 'update', 'crawl_update')
    def get():
        dbUserData = MongoDbManager().get_all_womancat_collection({})
        responseData = []
        for Data in dbUserData:
            Data = {k: Data[k] for k in show_index}
            # 차후수정부분
            responseData.append(Data)
        settings = MongoDbManager().get_setcat({"_id": "catsettings"})
        setting =[]
        for set in settings:
            setting.append(set)
        responseData.append(setting)
        return HttpResponse(json.dumps(responseData), status=200)

    if request.method == 'GET':
        return get()
    else:
        return HttpResponse(status=405)

def winner_db(request) :
    show_index = ('seller_name', 'title', 'ven_productcd', 'productid','rating','review', 'winner')
    def get():
        # pipeline = [{'$project': {'_id': 0}}]
        winproduct = []
        dbwinnerDate = MongoDbManager().get_winnerdb_from_collection({})
        for Data in dbwinnerDate[:100]:
            Data = {k: Data[k] for k in show_index}
            winproduct.append(Data)
        return HttpResponse(json.dumps(winproduct), status=200)

    if request.method == 'GET':
        return get()
    else:
        return HttpResponse(status=405)


