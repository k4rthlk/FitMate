from datetime import date

from django.db import models

from admin.models import tblcategory,Location


# Create your models here.

class Login(models.Model):
    loginid = models.AutoField(primary_key=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    status = models.CharField(max_length=50)


class User(models.Model):
    userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.BigIntegerField()
    address = models.CharField(max_length=100)
    userphoto = models.ImageField()
    phone = models.BigIntegerField()
    gender = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    regdate = models.DateField(default=date.today)
    catid = models.ForeignKey(tblcategory,on_delete=models.CASCADE,default="")
    locid = models.ForeignKey(Location, on_delete=models.CASCADE, default="")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, default="")
    status = models.CharField(max_length=100)



