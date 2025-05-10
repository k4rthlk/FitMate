from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

from admin.models import Location, tblcategory, District, Time, tblplan, Trainerassign, Trainer, tblequipment, Feedback
from guest.models import Login, User
from trainer.models import Planrequest, Timerequest, Workout, Diet


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if "loginid" in request.session:
        cat = User.objects.get(loginid_id=request.session['loginid'])
        userid = cat.userid

        trainer = Trainerassign.objects.get(userid=userid)
        trainerid = trainer.trainerid.trainerid

        pl = tblplan.objects.filter(catid=cat.catid)
        name = request.session.get('uname')

        tob = Planrequest.objects.filter(userid=userid).last()
        return render(request, "user/index.html",
                      {'pl': pl, 'bu': cat, 'trainerid': trainerid, 'userid': userid, 'tob': tob, 'name': name})
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if "loginid" in request.session:
        del request.session["loginid"]
        del request.session['uname']
        return redirect('/')
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


#
# def index(request):
#     cat = User.objects.get(loginid_id=request.session['loginid'])
#     userid = cat.userid
#     check = Trainerassign.objects.filter(userid=userid)
#     if check == 1:
#         trainer = Trainerassign.objects.get(userid=userid)
#         trainerid = trainer.trainerid.trainerid
#     else:
#         trainerid = 0
#     pl = tblplan.objects.filter(catid=cat.catid)
#     name = request.session.get('uname')
#
#     tob = Planrequest.objects.filter(userid=userid).last()
#     u = User.objects.get(status='assigned')
#     return render(request, "user/index.html",
#                   {'pl': pl, 'cat': cat, 'trainerid': trainerid, 'userid': userid, 'tob': tob, 'name': name , 'u':u})


# def index(request):
#     # Get the user's information
#     user_info = User.objects.get(loginid_id=request.session['loginid'])
#     cat = User.objects.get(loginid_id=request.session['loginid'])
#     userid = user_info.userid
#     name = request.session.get('uname')
#
#     # Get the trainer assigned to the user
#     trainer_assign = Trainerassign.objects.get(userid=userid)
#     trainer_id = trainer_assign.trainerid.trainerid
#
#     # Check if the user has a confirmed plan request
#     confirmed_plan = Planrequest.objects.filter(userid=userid, status="Confirmed").exists()
#
#     if confirmed_plan:
#         # User has a confirmed plan, display a message indicating so
#         return render(request, "user/index.html", {'on_plan': True, 'name': name,'cat':cat})
#     else:
#         # User does not have a confirmed plan, fetch and display available plans
#         plans = tblplan.objects.filter(catid=user_info.catid)
#         return render(request, "user/index.html", {'plans': plans, 'name': name,'cat':cat})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registration(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            if Login.objects.filter(email=email).exists():
                return HttpResponse(
                    "<script>alert('Email already exist.');window.location='/user/registration';</script>")

            loginobj = Login()
            loginobj.email = email
            loginobj.password = password
            loginobj.role = 'user'
            loginobj.status = 'confirmed'
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

            uobj.locid = Location.objects.get(locid=request.POST.get('location'))
            uobj.catid = tblcategory.objects.get(catid=request.POST.get('catname'))

            uobj.loginid = loginobj
            uobj.save()

            return HttpResponse("<script>alert('User registered');window.location='/guest/login';</script>")
        else:
            district = District.objects.all()
            cat = tblcategory.objects.all()

            return render(request, 'user/registration.html', {'district': district, 'cat': cat})
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


# def schedule(request):
#     ti = Time.objects.all()
#     cat = User.objects.get(loginid_id=request.session['loginid'])
#     tob = Planrequest.objects.filter(userid=cat.userid, status="Confirmed").first()
#     return render(request, "user/schedule.html", {'ti': ti, 'cat': cat, 'tob': tob})


# def schedule(request):
#     tob = Planrequest.objects.filter(userid=User.objects.get(loginid__loginid=request.session['loginid']), status="Confirmed").first()
#     ti = Time.objects.all()
#     mob = Timerequest.objects.filter(userid=User.objects.get(loginid__loginid=request.session['loginid']), status__in=("Confirmed","Requested"))
#     # cat = User.objects.get(loginid_id=request.session['loginid'])
#     # userid = cat.userid
#     # # return HttpResponse(userid)
#     # tob = Planrequest.objects.filter(userid=userid, status="Confirmed").first()
#     # mob = Timerequest.objects.filter(userid=userid, status="Confirmed")
#     # if request.method == 'POST':
#     #     existing_request = Timerequest.objects.filter(userid=cat.userid, status='Requested').exists()
#     #
#     #     if existing_request:
#     #         return HttpResponse(
#     #             "<script>alert('You Have Already Requested a Time Slot!');window.location='/user/schedule';</script>")
#     #
#     #     userid = request.POST.get('userid')
#     #     trainerid = request.POST.get('trainerid')
#     #
#     #     timerequest = Timerequest.objects.create(timeid_id=request.POST.get('timeid'), trainerid_id=trainerid,
#     #                                              userid_id=userid, status='Requested')
#     #     timerequest.save()
#
#         # return HttpResponse("<script>alert('Time slot requested successfully!');window.location='/user/schedule';</script>"), 'cat': cat, , 'mob': mob
#
#     return render(request, "user/schedule.html", {'ti': ti,'tob': tob,'mob': mob})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def equipmentview(request):
    if "loginid" in request.session:
        cat = User.objects.get(loginid_id=request.session['loginid'])
        eqp = tblequipment.objects.all()
        return render(request, "user/equipmentview.html", {'eqp': eqp, 'bu': cat})
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def schedule(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            userid = request.POST.get('userid')
            trainerid = request.POST.get('trainerid')
            timeid = request.POST.get('timeid')

            timerequest = Timerequest.objects.create(timeid_id=timeid, trainerid_id=trainerid, userid_id=userid,
                                                     status='Requested')
            timerequest.save()

            return HttpResponse(
                "<script>alert('Time slot requested successfully!');window.location='/user/schedule';</script>")

        tob = Planrequest.objects.filter(userid=User.objects.get(loginid__loginid=request.session['loginid']),
                                         status="Confirmed").first()
        ti = Time.objects.all()
        mob = Timerequest.objects.filter(userid=User.objects.get(loginid__loginid=request.session['loginid']),
                                         status__in=("Confirmed", "Requested"))
        cat = User.objects.get(loginid_id=request.session['loginid'])

        return render(request, "user/schedule.html", {'ti': ti, 'tob': tob, 'mob': mob, 'bu': cat})
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    if "loginid" in request.session:
        cat = User.objects.get(loginid_id=request.session['loginid'])
        return render(request, "user/profile.html", {'bu': cat})
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def useredit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            obj = User.objects.get(userid=id)
            obj.name = request.POST.get('name')
            obj.address = request.POST.get('address')
            obj.phone = request.POST.get('phone')
            obj.gender = request.POST.get('gender')
            obj.height = request.POST.get('height')
            obj.weight = request.POST.get('weight')

            if len(request.FILES) == 0:
                obj.userphoto = request.POST.get('userphoto')
            else:
                obj.userphoto = request.FILES['userpic']

            obj.save()
            return profile(request)
        cat = User.objects.get(loginid_id=request.session['loginid'])
        tobj = User.objects.get(userid=id)
        return render(request, "user/useredit.html", {'tobj': tobj, 'bu': cat})
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def applied(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            userid = request.POST.get('userid')
            trainerid = request.POST.get('trainerid')
            planrequestobj = Planrequest()
            planrequestobj.trainerid = Trainer.objects.get(trainerid=trainerid)
            planrequestobj.userid = User.objects.get(userid=userid)
            planrequestobj.planid = tblplan.objects.get(planid=id)
            planrequestobj.status = 'Requested';
            if Planrequest.objects.filter(userid=userid, status='requested').exists():
                return HttpResponse(
                    "<script>alert('Already Applied pls wait for the Trainer Confirmation');window.location='/user/index';</script>")
            planrequestobj.save()
            if Planrequest.objects.filter(userid=userid, planid=userid).exists():
                return HttpResponse(
                    "<script>alert('One Plan is already in Request');window.location='/user/index';</script>")
            planrequestobj.save()
            return HttpResponse("<script>alert('Requested');window.location='/user/index';</script>")
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


# def workoutview(request):
#     ti = Workout.objects.all()
#     cat = User.objects.get(loginid_id=request.session['loginid'])
#     tob = Planrequest.objects.filter(userid=cat.userid, status="Confirmed").first()
#     return render(request, "user/workoutview.html", {'ti': ti, 'cat': cat, 'tob': tob})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def workoutview(request):
    if "loginid" in request.session:
        cat = User.objects.get(loginid_id=request.session['loginid'])

        tob = Planrequest.objects.filter(userid=cat.userid, status="Confirmed").first()

        if tob:
            ti = Workout.objects.filter(planid_id=tob.planid_id)
        else:
            ti = None

        return render(request, "user/workoutview.html", {'ti': ti, 'tob': tob, 'bu': cat})
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def trainerview(request):
    if "loginid" in request.session:
        cat = User.objects.get(loginid_id=request.session['loginid'])
        mob = User.objects.get(loginid=cat.loginid)
        tob = Trainerassign.objects.get(userid=cat.userid)

        return render(request, "user/trainerview.html", {'tob': tob, 'mob': mob, 'bu': cat})
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dietview(request):
    if "loginid" in request.session:
        cat = User.objects.get(loginid_id=request.session['loginid'])

        tob = Planrequest.objects.filter(userid=cat.userid, status="Confirmed").first()

        if tob:
            ti = Diet.objects.filter(userid=tob.userid)
        else:
            ti = None

        return render(request, "user/dietview.html", {'ti': ti, 'bu': cat, 'tob': tob})
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changepassword(request):
    if "loginid" in request.session:
        cat = User.objects.get(loginid_id=request.session['loginid'])
        if request.method == 'POST':
            uname = request.POST.get("email")
            password = request.POST.get("password")
            newpwd = request.POST.get("newpwd")
            connewpwd = request.POST.get("connewpwd")
            if Login.objects.filter(email=uname, password=password).exists():
                lo = Login.objects.get(email=uname, password=password)
                if newpwd == connewpwd:
                    lo.password = newpwd
                    lo.save()
                    return HttpResponse(
                        "<script>alert('Successfully updated!!');window.location='/user/changepassword'</script>")
                return HttpResponse(
                    "<script>alert('Password Mismatch !!');window.location='/user/changepassword'</script>")
            return HttpResponse(
                "<script>alert('Invalid Username orPassword!!');window.location='/user/changepassword'</script>")
        return render(request, "user/changepassword.html", {'bu': cat})
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")


# def feedback(request):
#     cat = User.objects.get(loginid_id=request.session['loginid'])
#     if request.method == 'POST':
#         feed = request.POST.get('feedback')
#         userid = request.po
#         eqobj = Feedback()
#         if Feedback.objects.filter(userid=cat).exists():
#             return HttpResponse("<script>alert('Duplicate. ');window.location = 'feedback.html'</script>")
#         eqobj.description = feed
#
#
#         eqobj.save()
#
#         return HttpResponse("<script>alert('Inserted. ');window.location = '/user/feedback'</script>")
#     else:
#         return render(request, "user/feedback.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedback(request, id):
    if "loginid" in request.session:
        if request.method == "POST":
            loginid = request.session['loginid']
            ton = User.objects.get(loginid=loginid)
            userid = ton.userid
            tun = Feedback()
            tun.trainerid = Trainer.objects.get(trainerid=request.POST.get('trainer'))
            tun.userid = User.objects.get(userid=userid)
            tun.feedback = request.POST.get('feedback')
            tun.save()
            return HttpResponse("<script>alert('Inserted. ');window.location = '/user/trainerview/'</script>")
        tbl = Trainer.objects.get(trainerid=id)
        cat = User.objects.get(loginid_id=request.session['loginid'])
        return render(request, "user/feedback.html", {'tbl': tbl,'bu': cat })
    else:
        return HttpResponse("<script>alert('You need to Login First..');window.location='/login/';</script>")