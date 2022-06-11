from django.urls import path
from main import views
from main.Api import JsonTest

urlpatterns =[

    path('', views.login, name="login"),
    path('index/', views.index, name="index"),
    path('winproduct/', views.winproduct, name='winproduct'),
    path('winseller/', views.winseller, name='winseller'),
    path('productdb/', views.productdb, name='productdb'),
    path('sellerdb/', views.sellerdb, name='sellerdb'),
    path('catdb/', views.catdb, name='catdb'),
    path('catdb/man', views.catdb, name='catdb'),
    path('catdb/woman', views.womancatdb, name='womancatdb'),
    path('register/', views.register, name="register"),
    path('setting/', views.setting, name='setting'),
    path('setting/product', views.setting, name='product'),
    path('setting/seller', views.setting_seller, name='seller'),
    path('setting/category', views.setting_category, name='category'),
    path('setting/register/', views.register, name='register'),
    path('setting/sellersetting/', views.seller_register, name='sellersetting'),
    path('logout/', views.logout, name='logout'),
    path('winproduct/json', JsonTest.winner_db, name='JsonAllwinnerdb'),
    path('productdb/json', JsonTest.all_productdb, name='JsonAllproductdb'),
    path('sellerdb/json/', JsonTest.all_sellerdb, name='JsonAllsellerdb'),
    path('mancatdb/json/', JsonTest.man_category, name='JsonAllmancatdb'),
    path('womancatdb/json/', JsonTest.woman_category, name='JsonAllwomancatdb'),
    #path('productdb/delete', JsonTest.delete_productdb, name='Jsondeleteproductdb'),
]
