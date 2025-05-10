import random
import smtplib
import string
from email.message import EmailMessage

from django.http import HttpResponse
from django.shortcuts import render, redirect

from admin.models import District, Location, tblcategory
from guest.models import Login, User


# Create your views here.
def index(request):
    return render(request, "guest/index.html")


def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('pass')
        if Login.objects.filter(email=email, password=password).exists():
            loginobj = Login.objects.get(email=email, password=password)
            request.session['uname'] = loginobj.email
            request.session['loginid'] = loginobj.loginid
            role = loginobj.role
            status = loginobj.status
            if role == 'Admin':
                return redirect('/admin/adminindex')
            elif role == 'user' and status == "confirmed":
                return redirect('/user/index')
            elif role == 'trainer':
                return redirect('/trainer/trainerindex')

            else:
                return HttpResponse(
                    "<script>alert('Not an authorized person please wait until you are assigned ');window.location='/login/';</script>")
        else:
            return HttpResponse(
                "<script>alert('Invalid username or password');window.location='/login/';</script>")
    else:
        return render(request, "guest/login.html")


def userregistration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Login.objects.filter(email=email).exists():
            return HttpResponse(
                "<script>alert('Email already exist.');window.location='/userregistration';</script>")

        loginobj = Login()
        loginobj.email = email
        loginobj.password = password
        loginobj.role = 'user'
        loginobj.status = 'not assigned'
        loginobj.save()

        uobj = User()
        uobj.name = request.POST.get('name')
        uobj.address = request.POST.get('address')
        uobj.age = request.POST.get('age')
        uobj.phone = request.POST.get('phone')
        uobj.gender = request.POST.get('gender')
        uobj.userphoto = request.FILES['pic']
        uobj.height = request.POST.get('height')
        uobj.weight = request.POST.get('weight')
        uobj.status = 'not assigned'

        uobj.locid = Location.objects.get(locid=request.POST.get('location'))
        uobj.catid = tblcategory.objects.get(catid=request.POST.get('catname'))

        uobj.loginid = loginobj
        uobj.save()

        return HttpResponse("<script>alert('User registered');window.location='/login/';</script>")
    else:
        district = District.objects.all()
        cat = tblcategory.objects.all()

        return render(request, 'guest/userregistration.html', {'district': district, 'cat': cat})


def forgotpassword(request):
    if request.method == 'POST':
        uname = request.POST.get("Email")
        if Login.objects.filter(email=uname).exists():
            lg = Login.objects.get(email=uname)
            lid = lg.loginid
            cust = Login.objects.get(loginid=lid)
            email = cust.email
            obj=User.objects.get(loginid_id=cust.loginid)
            customer_name = obj.name
            characters = string.ascii_letters + string.digits
            random_number = ''.join(random.choice(characters) for _ in range(8))
            lg.password = random_number
            lg.save()
            msg = EmailMessage()
            msg.set_content(f'Hi {customer_name},Your new password to login in is {random_number}')
            msg['Subject'] = "Forgot Password ?"
            msg['from'] = 'jaguargaming123456i@gmail.com'
            msg['To'] = {email}
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('jaguargaming123456i@gmail.com', 'mbft wotm klho hfmu')
                smtp.send_message(msg)
                return HttpResponse("<script>alert('Login with new password in your email');window.location='/login';</script>")
        return HttpResponse("<script>alert('No datafound');window.location=' /forgotpassword';</script>")
    return render(request, "guest/forgotpassword.html")
