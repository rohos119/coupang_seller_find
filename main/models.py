from django.db import models
from django import forms
from django.contrib.auth.models import User
from mongoengine import *
import pymongo


# class ProductDB(Document):
#     seller_name = StringField(max_length=100)
#     title = StringField(max_length=300)
#     disc_price = StringField(max_length=10)
#     ven_prodctcd = StringField(max_length=50)
#     productid= StringField(max_length=20)
#     vendorid = StringField(max_length=20)
#     updatetime = DateTimeField()
#
#     def __init__(self):
#         mongodb = pymongo.MongoClient('mongodb+srv://admin:admin@coupangtest-ribq2.mongodb.net/test?retryWrites=true&w=majority')
#         product_db = mongodb.get_database('coupang').get_collection('product_db').find({}, {'productid', 'vendorid'})
#         for result in product_db:
#             self.seller_name = result['seller_name']

class WebUser(models.Model):
    userauth = models.CharField(max_length=10, auto_created="user")
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    update = models.DateTimeField(auto_now_add=True)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','first_name']

class LoginForm(forms.ModelForm) :
    class Meta:
        model = User
        fields = ['username','password']

class myseller(models.Model) :
    SELLER_TYPE = (
        ('1', '매칭셀러'),
        ('2', '자사셀러'),
        ('3', '제휴셀러'),)
    sellertype = models.CharField(max_length=5, choices=SELLER_TYPE)
    sellername = models.CharField(max_length=100)
    sellercode = models.CharField(max_length=50)
    update = models.DateTimeField(auto_now_add=True)

class sellerDB(forms.ModelForm) :
    class Meta:
        model= myseller
        fields =['sellertype' , 'sellername', 'sellercode']

class cateSet(forms.Form) :
    manual = models.CharField(max_length=10, auto_created="user")
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    update = models.DateTimeField(auto_now_add=True)

