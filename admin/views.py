import smtplib
from email.message import EmailMessage

import xlwt
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.cache import cache_control

from admin.models import District, Location, tblequipment, tblcategory, tblplan, Trainer, Trainerassign, Time, Feedback
from guest.models import User, Login
from trainer.models import Planrequest, Timerequest, Diet


# Create your views here.




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if "loginid" in request.session:

        labels = []
        data = []

        queryset = Planrequest.objects.filter(status='Confirmed').values('planid__planname').annotate(
            total_plans=Count('planassignid'))
        for s in queryset:
            labels.append(s['planid__planname'])
            data.append(s['total_plans'])

        return render(request, 'admin/index.html', {
            'labels': labels,
            'data': data,
        })

        return render(request, "admin/index.html")

    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if "loginid" in request.session:
        del request.session["loginid"]
        del request.session['uname']
        return redirect('/')
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def districtreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            disname = request.POST.get('disname')
            depobj = District()
            if District.objects.filter(disname=disname).exists():
                return HttpResponse("<script>alert('Duplicate. ');window.location = 'districtreg.html'</script>")
            depobj.disname = disname
            depobj.save()

            return HttpResponse("<script>alert('Inserted. ');window.location = '/admin/districtreg'</script>")

        return render(request, "admin/districtreg.html")
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def districtview(request):
    if "loginid" in request.session:
        depobj = District.objects.all()
        return render(request, "admin/districtview.html", {'depobj': depobj})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def districtedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            disname = request.POST.get('disname')
            depobj = District.objects.get(disid=id)
            depobj.disname = disname
            depobj.save()
            return districtview(request)
        depobj = District.objects.get(disid=id)
        return render(request, "admin/districtedit.html", {'depobj': depobj})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


# def districtdelete(request, id):
#     dist = District.objects.get(disid=id)
#     dist.delete()
#     return districtview(request)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def locationreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            locname = request.POST.get('locname')
            dist = request.POST.get('disname')

            loc_obj = Location()
            if Location.objects.filter(locname=locname).exists():
                return HttpResponse("<script>alert('Duplicate..');window.location ='/admin/locationreg';</script>")
            loc_obj.locname = locname
            loc_obj.disid = District.objects.get(disid=dist)
            loc_obj.save()
            return HttpResponse("<script>alert('Inserted..');window.location ='/admin/locationreg';</script>")
        else:
            district = District.objects.all()
            return render(request, "admin/locationreg.html", {'district': district})

    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def locationview(request):
    if "loginid" in request.session:
        district = District.objects.all()
        row = District.objects.first()
        # return HttpResponse(row.disname)
        location = Location.objects.filter(disid=row.disid)

        return render(request, 'admin/locationview.html', {'district': district, 'location': location})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filllocation(request):
    if "loginid" in request.session:
        disid = int(request.POST.get("districtid"))
        location = Location.objects.filter(disid=disid).values()

        return JsonResponse(list(location), safe=False)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def locationedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            districtid = District.objects.get(disid=request.POST.get('districtid'))
            locationname = request.POST.get('locationname')
            locationobj = Location.objects.get(locid=id)
            if Location.objects.filter(locname=locationname, disid=districtid).exists():
                return HttpResponse("<script>alert('Already exist');window.location='/admin/viewlocation';</script>")
            locationobj.locname = locationname
            locationobj.disid = districtid
            locationobj.save()
            return locationview(request)
        else:
            district = District.objects.all()
            location = Location.objects.get(locid=id)
            return render(request, 'admin/locationedit.html', {'location': location, 'district': district})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

# def locationdelete(request, id):
#     loc = Location.objects.get(locid=id)
#     loc.delete()
#     return locationview(request)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def equipmentreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            eqname = request.POST.get('eqname')
            eqpic = request.FILES['eqpic']
            desc = request.POST.get('desc')
            quantity = request.POST.get('quantity')
            eqobj = tblequipment()
            if tblequipment.objects.filter(equipname=eqname).exists():
                return HttpResponse("<script>alert('Duplicate. ');window.location = 'equipmentreg.html'</script>")
            eqobj.equipname = eqname
            eqobj.equipphoto = eqpic
            eqobj.description = desc
            eqobj.quantity = quantity

            eqobj.save()

            return HttpResponse("<script>alert('Inserted. ');window.location = '/admin/equipmentreg'</script>")
        else:
            return render(request, "admin/equipmentreg.html")
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def equipmentview(request):
    if "loginid" in request.session:
        eqp = tblequipment.objects.all()
        return render(request, "admin/equipmentview.html", {'eqp': eqp})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def equipmentedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            equipname = request.POST.get('equipname')

            regdate = request.POST.get('regdate')
            description = request.POST.get('description')
            quantity = request.POST.get('quantity')
            eqp = tblequipment.objects.get(equipid=id)
            eqp.equipname = equipname
            eqp.regdate = regdate
            eqp.description = description
            eqp.quantity = quantity
            if len(request.FILES) == 0:
                eqp.equipphoto = request.POST.get('equipphoto')
            else:
                eqp.equipphoto = request.FILES['equippic']
            eqp.save()
            return equipmentview(request)
        eqp = tblequipment.objects.get(equipid=id)
        return render(request, "admin/equipmentedit.html", {'eqp': eqp})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def equipmentdelete(request, id):
    if "loginid" in request.session:
        eqp = tblequipment.objects.get(equipid=id)
        eqp.delete()
        return equipmentview(request)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categoryreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            catname = request.POST.get('catname')
            catobj = tblcategory()
            if tblcategory.objects.filter(catname=catname).exists():
                return HttpResponse("<script>alert('Duplicate. ');window.location = 'categoryreg.html'</script>")
            catobj.catname = catname
            catobj.save()

            return HttpResponse("<script>alert('Inserted. ');window.location = '/admin/categoryreg'</script>")

        return render(request, "admin/categoryreg.html")
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categoryview(request):
    if "loginid" in request.session:
        cat = tblcategory.objects.all()
        return render(request, "admin/categoryview.html", {'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categoryedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            catname = request.POST.get('catname')
            catobj = tblcategory.objects.get(catid=id)
            catobj.catname = catname
            catobj.save()
            return categoryview(request)
        catobj = tblcategory.objects.get(catid=id)
        return render(request, "admin/categoryedit.html", {'catobj': catobj})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categorydelete(request, id):
    if "loginid" in request.session:
        cat = tblcategory.objects.get(catid=id)
        cat.delete()
        return categoryview(request)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def planreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            planname = request.POST.get('planname')
            price = request.POST.get('price')
            val = request.POST.get('val')
            desc = request.POST.get('desc')
            catid = tblcategory.objects.get(catid=request.POST.get('catid'))
            pobj = tblplan()
            if tblplan.objects.filter(planname=planname).exists():
                return HttpResponse("<script>alert('Duplicate. ');window.location = 'planreg.html'</script>")
            pobj.planname = planname
            pobj.price = price
            pobj.validity = val
            pobj.description = desc
            pobj.catid = catid
            pobj.save()

            return HttpResponse("<script>alert('Inserted. ');window.location = '/admin/planreg'</script>")
        else:
            cat = tblcategory.objects.all()
            return render(request, "admin/planreg.html", {'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def planview(request):
    if "loginid" in request.session:
        cat = tblcategory.objects.all()
        row = tblcategory.objects.first()
        plan = tblcategory.objects.filter(catid=row.catid)
        return render(request, 'admin/planview.html', {'cat': cat, 'plan': plan})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillplan(request):
    if "loginid" in request.session:
        catid = int(request.POST.get("catid"))
        plan = tblplan.objects.filter(catid=catid).values()

        return JsonResponse(list(plan), safe=False)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def planedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            catid = tblcategory.objects.get(catid=request.POST.get('catid'))
            planname = request.POST.get('planname')
            price = request.POST.get('price')
            validity = request.POST.get('validity')
            desc = request.POST.get('desc')
            pobj = tblplan.objects.get(planid=id)
            if tblplan.objects.filter(planname=planname, catid=catid).exists():
                return HttpResponse("<script>alert('Already exist');window.location='/admin/locationview';</script>")
            pobj.planname = planname
            pobj.price = price
            pobj.validity = validity
            pobj.description = desc
            pobj.catid = catid
            pobj.save()
            return planview(request)
        else:
            cat = tblcategory.objects.all()
            plan = tblplan.objects.get(planid=id)
            return render(request, 'admin/planedit.html', {'cat': cat, 'plan': plan})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def plandelete(request, id):
    if "loginid" in request.session:
        plan = tblplan.objects.get(planid=id)
        plan.delete()
        return planview(request)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userview(request):
    if "loginid" in request.session:
        usr = User.objects.all()
        return render(request, "admin/userview.html", {'usr': usr})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


# def useredit(request, id):
#     if request.method == 'POST':
#
#         tobj = User.objects.get(userid=id)
#         tobj.name = request.POST.get('name')
#         tobj.address = request.POST.get('address')
#         tobj.regdate = request.POST.get('regdate')
#         tobj.phone = request.POST.get('phone')
#         tobj.gender = request.POST.get('gender')
#         tobj.height = request.POST.get('heght')
#         tobj.weight = request.POST.get('weight')
#
#         if len(request.FILES) == 0:
#             tobj.userphoto = request.POST.get('userphoto')
#         else:
#             tobj.userphoto = request.FILES['userpic']
#
#         tobj.save()
#         return userview(request)
#     tobj = User.objects.get(userid=id)
#     return render(request, "admin/useredit.html", {'tobj': tobj})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userdelete(request, id):
    if "loginid" in request.session:
        user = User.objects.get(userid=id)
        user.delete()
        return userview(request)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def trainerreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            if Login.objects.filter(email=email).exists():
                return HttpResponse("<script>alert('Email already exist.');window.location='/admin/trainerreg';</script>")

            loginobj = Login()
            loginobj.email = email
            loginobj.password = password
            loginobj.role = 'trainer'
            loginobj.status = 'confirmed'
            loginobj.save()

            tobj = Trainer()
            tobj.name = request.POST.get('name')
            tobj.address = request.POST.get('address')
            tobj.phone = request.POST.get('phone')
            tobj.age = request.POST.get('age')
            tobj.gender = request.POST.get('gender')
            tobj.trainerphoto = request.FILES['pic']
            tobj.experience = request.POST.get('exp')

            tobj.locid = Location.objects.get(locid=request.POST.get('location'))
            tobj.catid = tblcategory.objects.get(catid=request.POST.get('catname'))

            tobj.loginid = loginobj
            tobj.save()

            return HttpResponse("<script>alert('trainer registered');window.location='/admin/trainerreg';</script>")
        else:
            district = District.objects.all()
            cat = tblcategory.objects.all()

            return render(request, 'admin/trainerreg.html', {'district': district, 'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def trainerview(request):
    if "loginid" in request.session:
        tr = Trainer.objects.all()
        return render(request, "admin/trainerview.html", {'tr': tr})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def traineredit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            tobj = Trainer.objects.get(trainerid=id)
            tobj.name = request.POST.get('trainername')
            tobj.address = request.POST.get('address')
            tobj.age = request.POST.get('age')
            tobj.phone = request.POST.get('phone')
            tobj.experience = request.POST.get('experience')
            if len(request.FILES) == 0:
                tobj.trainerphoto = request.POST.get('trainerphoto')
            else:
                tobj.trainerphoto = request.FILES['trainerpic']
            # return HttpResponse(request.POST.get('trainerphoto'))
            tobj.save()
            return trainerview(request)
        tobj = Trainer.objects.get(trainerid=id)
        return render(request, "admin/traineredit.html", {'tobj': tobj})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def trainerdelete(request, id):
    if "loginid" in request.session:
        trainer = Trainer.objects.get(trainerid=id)
        trainer.delete()
        return trainerview(request)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def trainerassign(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            user = request.POST.get('uname')
            us = User.objects.get(userid=user)
            log = us.loginid.loginid
            login = Login.objects.get(loginid=log)
            email = login.email
            # return HttpResponse(email)
            login.status = "confirmed"
            login.save()
            tobj = Trainerassign()
            tobj.userid = User.objects.get(userid=request.POST.get('uname'))
            tobj.trainerid = Trainer.objects.get(trainerid=request.POST.get('tname'))
            teobj = User.objects.get(userid=user)
            tobj.userid = teobj
            tobj.save()
            ttobj = User.objects.get(userid=teobj.userid)
            ttobj.status = "assigned"
            ttobj.save()
            msg = EmailMessage()
            msg.set_content('Confirmed')
            msg['Subject'] = "Test"
            msg['from'] = 'jaguargaming123456i@gmail.com'
            msg['To'] = email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('jaguargaming123456i@gmail.com', 'mbft wotm klho hfmu')
                smtp.send_message(msg)
                return HttpResponse("<script>alert('send');window.location = '/admin/trainerassign'</script>")

            # return HttpResponse("<script>alert('Assigned. ');window.location = '/admin/trainerassign'</script>")
        else:
            user = User.objects.filter(status="not assigned")
            return render(request, "admin/trainerassign.html", {'user': user})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillassign(request):
    if "loginid" in request.session:
        userid = int(request.POST.get("user"))
        user = User.objects.get(userid=userid)
        catid = user.catid.catid
        trainer = Trainer.objects.filter(catid=catid).values()
        return JsonResponse(list(trainer), safe=False)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def timereg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            time = request.POST.get('time')
            tobj = Time()

            if Time.objects.filter(time=time).exists():
                return HttpResponse("<script>alert('Duplicate. ');window.location = '/admin/timereg'</script>")
            tobj.time = time
            tobj.meredium = request.POST.get('meredium')
            tobj.save()

            return HttpResponse("<script>alert('Inserted. ');window.location = '/admin/timereg'</script>")

        return render(request, "admin/timereg.html")
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def timeview(request):
    if "loginid" in request.session:
        meridium = Time.objects.all()
        row = Time.objects.first()
        timeid = Time.objects.filter(meredium=row.meredium)
        return render(request, 'admin/timeview.html', {'meridium': meridium, 'timeid': timeid})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filltime(request):
    if "loginid" in request.session:
        timeid = request.POST.get("timeid")
        location = Time.objects.filter(meredium=timeid).values()
        return JsonResponse(list(location), safe=False)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def timeedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            time = request.POST.get('time')
            meridium = request.POST.get('meredium')
            tobj = Time.objects.get(timeid=id)
            tobj.time = time
            tobj.meredium = meridium
            tobj.save()
            return timeview(request)
        tobj = Time.objects.get(timeid=id)
        return render(request, "admin/timeedit.html", {'tobj': tobj})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def timedelete(request, id):
    if "loginid" in request.session:
        time = Time.objects.get(timeid=id)
        time.delete()
        return timeview(request)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reassign(request):
    if "loginid" in request.session:
        assigned = Trainerassign.objects.all()
        return render(request, "admin/reassign.html", {'assigned': assigned})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reassignedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            trainer = request.POST.get('trainer')
            user = request.POST.get('user')
            eqp = Trainerassign.objects.get(userid=user)
            eqp.trainerid = Trainer.objects.get(trainerid=trainer)
            eqp.save()
            plan = Planrequest.objects.get(userid=user)
            plan.trainerid = Trainer.objects.get(trainerid=trainer)
            plan.save()
            time = Timerequest.objects.get(userid=user)
            time.trainerid = Trainer.objects.get(trainerid=trainer)
            time.save()
            diet = Diet.objects.get(userid=user)
            diet.trainerid = Trainer.objects.get(trainerid=trainer)
            diet.save()
            return HttpResponse("<script>alert('Inserted. ');window.location = '/admin/reassign/'</script>")
        eqp = Trainerassign.objects.get(userid=id)
        user = User.objects.get(userid=id)
        catid = user.catid.catid
        trainer = Trainer.objects.filter(catid=catid).values()
        return render(request, "admin/reassignedit.html", {'eqp': eqp, 'trainer': trainer})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reportplan(request):
    if "loginid" in request.session:
        labels = []
        data = []

        queryset = Planrequest.objects.filter(status='Confirmed').values('planid__planname').annotate(total_plans=Count('planassignid'))
        for s in queryset:
            labels.append(s['planid__planname'])
            data.append(s['total_plans'])

        return render(request, 'Admin/reportplan.html', {
            'labels': labels,
            'data': data,
        })
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def locwiseuser(request):
    if "loginid" in request.session:
        district = District.objects.all()
        return render(request, "admin/locwiseuser.html", {"district":district})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userlocwise(request):
    if "loginid" in request.session:
        labels = []
        data = []
        district_id = request.POST.get('disname')

        # Query locations within the selected district
        locations = Location.objects.filter(disid=district_id)

        for location in locations:
            # Query candidate count for each location within the district
            candidate_count = User.objects.filter(locid=location.locid).count()
            labels.append(location.locname)
            data.append(candidate_count)
        #return HttpResponse(labels)
        return render(request, 'admin/userlocwise.html', {'labels': labels,'data':data})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filluserloc(request):
    if "loginid" in request.session:
        location = request.POST.get("loc")
        canid = User.objects.filter(userid=location).values()
        return JsonResponse(list(canid),safe=False)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def assignedusersxcel(request):
    if "loginid" in request.session:
        trainer = Trainer.objects.all()
        return render(request, "admin/assignedusersxcel.html", {'trainer': trainer})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filltrainersuser(request):
    if "loginid" in request.session:
        trainer_id = request.POST.get("trainer")
        users = Trainerassign.objects.filter(trainerid_id=trainer_id).values('userid__name','userid__loginid__email','userid__phone','userid__address','userid__age','userid__height','userid__weight')
        return JsonResponse(list(users), safe=False)
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


class ExportExcelUsers(View):
    def post(self, request):
        if "loginid" in request.session:
            tid=request.POST.get('trainerid')
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="userslist.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Sheet1')

            # Define the column headings
            row_num = 0
            columns = ['Name', 'Email','Phone','Address','Age', 'Height(CM)', 'Weight(KG)']
            for col_num, column_title in enumerate(columns):
                ws.write(row_num, col_num, column_title)

            # Query the data from your model, and write it to the worksheet
            queryset = Trainerassign.objects.filter(trainerid_id=tid).values_list('userid__name','userid__loginid__email','userid__phone','userid__address','userid__age','userid__height','userid__weight')
            for row in queryset:
                row_num += 1
                for col_num, cell_value in enumerate(row):
                    ws.write(row_num, col_num, cell_value)

            wb.save(response)
            return response
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedback(request):
    if "loginid" in request.session:
        feed = Feedback.objects.all()
        return render(request, "admin/feedback.html", {'feed': feed})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")
