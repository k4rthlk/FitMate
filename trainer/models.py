from django.db import models

from admin.models import tblplan, Trainer, Time
from guest.models import User


# Create your models here.
class Planrequest(models.Model):
    planassignid = models.AutoField(primary_key=True)
    trainerid = models.ForeignKey(Trainer, on_delete=models.CASCADE, default="")
    userid = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    planid = models.ForeignKey(tblplan, on_delete=models.CASCADE, default="")
    status = models.CharField(max_length=50)


class Timerequest(models.Model):
    timeassignid = models.AutoField(primary_key=True)
    trainerid = models.ForeignKey(Trainer, on_delete=models.CASCADE, default="")
    userid = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    timeid = models.ForeignKey(Time, on_delete=models.CASCADE, default="")
    status = models.CharField(max_length=50)


class Workout(models.Model):
    wid = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=500)
    planid = models.ForeignKey(tblplan, on_delete=models.CASCADE, default="")


class Diet(models.Model):
    dietid = models.AutoField(primary_key=True)
    diet = models.CharField(max_length=50)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    trainerid = models.ForeignKey(Trainer, on_delete=models.CASCADE, default="")
    status = models.CharField(max_length=50)
