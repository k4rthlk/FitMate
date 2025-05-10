from datetime import date

from django.db import models


# Create your models here.

class District(models.Model):
    disid = models.AutoField(primary_key=True)
    disname = models.CharField(max_length=50)


class Location(models.Model):
    locid = models.AutoField(primary_key=True)
    locname = models.CharField(max_length=50)
    disid = models.ForeignKey(District, on_delete=models.CASCADE, default="")


class tblequipment(models.Model):
    equipid = models.AutoField(primary_key=True)
    equipname = models.CharField(max_length=50)
    equipphoto = models.ImageField()
    regdate = models.DateField(default=date.today)
    description = models.CharField(max_length=50)
    quantity = models.BigIntegerField()


class tblcategory(models.Model):
    catid = models.AutoField(primary_key=True)
    catname = models.CharField(max_length=50)


class tblplan(models.Model):
    planid = models.AutoField(primary_key=True)
    planname = models.CharField(max_length=50)
    price = models.BigIntegerField()
    validity = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    catid = models.ForeignKey(tblcategory, on_delete=models.CASCADE, default="")


from guest.models import User, Login


class Trainer(models.Model):
    trainerid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.BigIntegerField()
    address = models.CharField(max_length=100)
    trainerphoto = models.ImageField()
    phone = models.BigIntegerField()
    gender = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    regdate = models.DateField(default=date.today)
    catid = models.ForeignKey(tblcategory, on_delete=models.CASCADE, default="")
    locid = models.ForeignKey(Location, on_delete=models.CASCADE, default="")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, default="")


class Trainerassign(models.Model):
    assignid = models.AutoField(primary_key=True)
    trainerid = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)


class Time(models.Model):
    timeid = models.AutoField(primary_key=True)
    time = models.CharField(max_length=50)
    meredium = models.CharField(max_length=50)

class Feedback(models.Model):
    feedbackid = models.AutoField(primary_key=True)
    feedback = models.CharField(max_length=50)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    trainerid = models.ForeignKey(Trainer, on_delete=models.CASCADE)