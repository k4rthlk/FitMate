from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Subquery, OuterRef
from django.views.decorators.cache import cache_control

from admin.models import Trainer, Trainerassign, tblplan, tblcategory
from guest.models import User
from trainer.models import Workout, Planrequest, Timerequest, Diet
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from decimal import Decimal


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if "loginid" in request.session:
        cat = Trainer.objects.get(loginid_id=request.session['loginid'])
        return render(request, "trainer/index.html", {'cat': cat})
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
def workoutreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            loginid = request.session.get('loginid')
            trainer = Trainer.objects.get(loginid=loginid)
            categoryid = trainer.catid.catid
            plan = tblplan.objects.filter(catid=categoryid)
            tobj = Workout()
            tobj.desc = request.POST.get('work')

            pid = request.POST.get('pname')
            tobj.planid = tblplan.objects.get(planid=pid)
            tobj.save()

            return HttpResponse("<script>alert('Workout registered');window.location='/trainer/workoutreg';</script>")

        else:
            loginid = request.session.get('loginid')
            trainer = Trainer.objects.get(loginid=loginid)
            categoryid = trainer.catid.catid
            plan = tblplan.objects.filter(catid=categoryid)
            cat = Trainer.objects.get(loginid_id=request.session['loginid'])
            return render(request, "trainer/workoutreg.html", {'plan': plan, 'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")



# def workoutview(request):
#     wobj = Workout.objects.all()
#     cat = Trainer.objects.get(loginid_id=request.session['loginid'])
#     return render(request,"trainer/workoutview.html",{'wobj':wobj, 'cat': cat})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def workoutview(request):
    if "loginid" in request.session:
        # Check if the user is logged in
        if 'loginid' not in request.session:
            return redirect('login')  # Redirect to the login page if not logged in

        # Get the Trainer object associated with the current session's login ID
        trainer = Trainer.objects.get(loginid_id=request.session['loginid'])

        # Get the Category ID associated with the Trainer
        category_id = trainer.catid_id

        # Filter Workout objects based on the Category ID
        wobj = Workout.objects.filter(planid__catid_id=category_id)
        cat = Trainer.objects.get(loginid_id=request.session['loginid'])

        return render(request, "trainer/workoutview.html", {'wobj': wobj, 'trainer': trainer, 'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


# def workoutedit(request,id):
#     if request.method == 'POST':
#         plan = tblcategory.objects.get(catid=request.POST.get('catid'))
#         workout = request.POST.get('workout')
#         wk = Workout.objects.get(wid=id)
#         if Workout.objects.filter(desc=workout, planid=catid).exists():
#             return HttpResponse("<script>alert('Already exist');window.location='/admin/viewlocation';</script>")
#         wk.locname = workout
#         wk.disid = catid
#         wk.save()
#         return workoutview(request)
#     else:
#         plan = tblplan.objects.all()
#         workout = Workout.objects.get(wid=id)
#         return render(request, 'trainer/workoutedit.html', {'workout': workout, 'plan': plan})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def workoutedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            # Retrieve the plan and category information based on the form data
            catid = request.POST.get('catid')
            try:
                plan = tblplan.objects.filter(catid=catid).first()  # Use filter() and first() to handle multiple objects
            except ObjectDoesNotExist:
                return HttpResponse("<script>alert('Plan not found.'); window.location='/trainer/workoutview';</script>")

            # Get the workout data from the form
            workout_desc = request.POST.get('workout')

            # Check if the workout description already exists for the same plan
            if Workout.objects.filter(desc=workout_desc, planid=plan).exists():
                return HttpResponse(
                    "<script>alert('Workout already exists for this plan.'); window.location='/trainer/workoutview';</script>")

            # Update the workout
            workout = Workout.objects.get(wid=id)
            workout.desc = workout_desc
            workout.planid = plan
            workout.save()

            return redirect('workoutview')  # Assuming 'workoutview' is your view function name
        else:
            # Fetch the plan options and the workout to be edited
            plans = tblplan.objects.all()
            workout = Workout.objects.get(wid=id)

            return render(request, 'trainer/workoutedit.html', {'workout': workout, 'plans': plans})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")



def workoutdelete(request, id):
    wc = Workout.objects.get(wid=id)
    wc.delete()
    return workoutview(request)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def planreq(request):
    if "loginid" in request.session:
        # Get the Trainer object associated with the current session's login ID
        trainer = Trainer.objects.get(loginid_id=request.session['loginid'])

        # Filter Planrequest objects based on the trainer's category ID
        plan_requests = Planrequest.objects.filter(trainerid_id=trainer.trainerid)
        cat = Trainer.objects.get(loginid_id=request.session['loginid'])
        return render(request, "trainer/planreq.html", {'plan_requests': plan_requests, 'trainer': trainer, 'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


# def requestview(request):
#     plan = Planrequest.objects.all()
#     cat = Trainer.objects.get(loginid_id=request.session['loginid'])
#     return render(request,"trainer/requestview.html",{'plan':plan, 'cat':cat})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def requestview(request):
    if "loginid" in request.session:
        # Get the Trainer object associated with the current session's login ID
        trainer = Trainer.objects.get(loginid_id=request.session['loginid'])

        plan_requests = Planrequest.objects.filter(trainerid_id=trainer.trainerid, status="Requested")

        for request_obj in plan_requests:
            # return HttpResponse(request_obj.userid)
            h = Decimal(request_obj.userid.height)
            weight = 100
            bmi = h - weight
            request_obj.bmi = bmi

        cat = Trainer.objects.get(loginid_id=request.session['loginid'])

        return render(request, "trainer/requestview.html", {'plan_requests': plan_requests, 'trainer': trainer, 'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def planconfirm(request, id):
    if "loginid" in request.session:
        plan = Planrequest.objects.get(planassignid=id)
        plan.status = 'Confirmed';
        plan.save()
        return HttpResponse("<script>alert('confirmed. ');window.location = '/trainer/requestview/'</script>")
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def requestreject(request, id):
    if "loginid" in request.session:
        plan = Planrequest.objects.get(planassignid=id)
        plan.status = 'Rejected';
        plan.save()
        return HttpResponse("<script>alert('Rejected..... ');window.location = '/trainer/requestview/'</script>")
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userview(request):
    if "loginid" in request.session:
        # Get the Trainer object associated with the current session's login ID
        trainer = Trainer.objects.get(loginid_id=request.session['loginid'])

        # Retrieve the users assigned to the trainer
        assigned_users = User.objects.filter(trainerassign__trainerid=trainer.trainerid)

        return render(request, "trainer/userview.html", {'usr': assigned_users, 'cat': trainer})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def timereq(request):
    if "loginid" in request.session:
        # Get the Trainer object associated with the current session's login ID
        trainer = Trainer.objects.get(loginid_id=request.session['loginid'])

        # Filter Planrequest objects based on the trainer's category ID
        time_requests = Timerequest.objects.filter(trainerid_id=trainer.trainerid)
        cat = Trainer.objects.get(loginid_id=request.session['loginid'])
        return render(request, "trainer/timereq.html", {'time_requests': time_requests, 'trainer': trainer, 'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def timereqview(request):
    if "loginid" in request.session:
        # Get the Trainer object associated with the current session's login ID
        trainer = Trainer.objects.get(loginid_id=request.session['loginid'])

        # Filter Planrequest objects based on the trainer's category ID
        time_requests = Timerequest.objects.filter(trainerid_id=trainer.trainerid, status="Requested")

        cat = Trainer.objects.get(loginid_id=request.session['loginid'])

        return render(request, "trainer/timereqview.html",
                      {'time_requests': time_requests, 'trainer': trainer, 'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def timeconfirm(request, id):
    if "loginid" in request.session:
        time = Timerequest.objects.get(timeassignid=id)
        time.status = 'Confirmed';
        time.save()
        return HttpResponse("<script>alert('confirmed. ');window.location = '/trainer/timereqview/'</script>")
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def timereject(request, id):
    if "loginid" in request.session:
        time = Timerequest.objects.get(timeassignid=id)
        time.status = 'Rejected';
        time.save()
        return HttpResponse("<script>alert('Rejected..... ');window.location = '/trainer/requestview/'</script>")
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


# def dietassign(request):
#     if request.method == 'POST':
#         cat = Trainer.objects.get(loginid_id=request.session['loginid'])
#
#         user_id = request.POST.get('uname')  # Assuming this is the user ID
#         diet = request.POST.get('diet')
#
#         diett = Diet()
#         diett.userid_id = user_id  # Assign the user ID, not the User object
#         diett.trainerid = cat
#         diett.diet = diet
#         diett.status = "assigned"
#         diett.save()
#
#         return redirect("<script>alert('Diet Assigned.... ');window.location = '/trainer/dietassign/'</script>")  # Redirect to the desired URL after successful assignment
#     else:
#         trainer_id = request.session.get('loginid')  # Assuming 'loginid' is the field representing the trainer's ID
#         trainer_assignments = Trainerassign.objects.filter(trainerid_id=trainer_id)
#         assigned_users = [assignment.userid for assignment in trainer_assignments if
#                           assignment.userid.status == "assigned"]
#         cat = Trainer.objects.get(loginid_id=request.session['loginid'])
#         cot = Trainer.objects.get(loginid=trainer_id)
#         tob = cot.trainerid
#         kob = Trainerassign.objects.filter(trainerid=tob)
#         # return HttpResponse(tob)
#         return render(request, "trainer/dietassign.html", {'assigned_users': assigned_users, 'cat': cat,'user':kob})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dietassign(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            cat = Trainer.objects.get(loginid_id=request.session['loginid'])

            user_id = request.session['uname']  # Assuming this is the user ID
            diet = request.POST.get('diet')

            diett = Diet()
            diett.userid_id = user_id  # Assign the user ID, not the User object
            diett.trainerid = cat
            diett.diet = diet
            diett.status = "assigned"
            diett.save()
            if 'dietdata' in request.session:
                del request.session['dietdata']
            return HttpResponse("<script>alert('Diet Assigned.... ');window.location = '/trainer/dietassign/'</script>")
        else:

            trainer_id = request.session.get('loginid')
            cat = Trainer.objects.get(loginid_id=request.session['loginid'])
            cot = Trainer.objects.get(loginid=trainer_id)
            tob = cot.trainerid
            subquery = Diet.objects.filter(userid=OuterRef('userid')).values('userid')
            kob = Trainerassign.objects.filter(trainerid=tob).exclude(
                userid__in=Subquery(subquery))
            return render(request, "trainer/dietassign.html",
                          {'cat': cat, 'user': kob})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


def filldietassign(request):
    userid = int(request.POST.get("userid"))
    user = User.objects.filter(userid=userid).values()
    return JsonResponse(list(user), safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dietassignedview(request):
    if "loginid" in request.session:
        # Get the Trainer object associated with the current session's login ID
        trainer = Trainer.objects.get(loginid_id=request.session['loginid'])

        # Filter Planrequest objects based on the trainer's category ID
        diet = Diet.objects.filter(trainerid_id=trainer.trainerid)
        cat = Trainer.objects.get(loginid_id=request.session['loginid'])
        return render(request, "trainer/dietassignedview.html", {'diet': diet, 'trainer': trainer, 'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def timeassignedview(request):
    if "loginid" in request.session:
        # Get the Trainer object associated with the current session's login ID
        trainer = Trainer.objects.get(loginid_id=request.session['loginid'])

        # Filter Planrequest objects based on the trainer's category ID
        time = Timerequest.objects.filter(trainerid_id=trainer.trainerid)
        cat = Trainer.objects.get(loginid_id=request.session['loginid'])
        return render(request, "trainer/timeassignedview.html", {'time': time, 'trainer': trainer, 'cat': cat})
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def predictdiet(request):
    if "loginid" in request.session:

        request.session['uname'] = request.POST.get('uname')
        diet_data = {
            'Age': [25, 26, 30, 35, 40, 45, 50, 55, 60],
            'Weight': [70, 71, 75, 80, 85, 90, 95, 100, 105],
            'Height': [170, 172, 174, 175, 178, 180, 182, 185, 188],
            'Exercise_Hours': [1, 2, 2, 3, 3, 2, 1, 1, 2],
            'Diet_Type': ['Low_Carb', 'Low_Carb', 'Balanced', 'Balanced', 'Low_Fat', 'Low_Fat', 'Balanced', 'Low_Carb',
                          'Balanced']
        }

        # Create DataFrame
        df = pd.DataFrame(diet_data)

        # Convert categorical variable into dummy/indicator variables
        df = pd.get_dummies(df, columns=['Diet_Type'])

        # Split features and target
        X = df.drop(['Diet_Type_Balanced', 'Diet_Type_Low_Carb', 'Diet_Type_Low_Fat'], axis=1)
        y = df[['Diet_Type_Balanced', 'Diet_Type_Low_Carb', 'Diet_Type_Low_Fat']]

        # Train the model
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)

        # Function to suggest meals based on diet type
        def suggest_meals(predicted_diet):
            diet_suggestions = {
                'Balanced': {
                    'breakfast': ['Whole grain toast with avocado and scrambled eggs', 'Fresh fruit',
                                  'Glass of milk or yogurt'],
                    'lunch': ['Grilled chicken salad with mixed greens, vegetables, nuts, and vinaigrette dressing',
                              'Whole grain roll'],
                    'dinner': ['Baked salmon with quinoa and steamed vegetables', 'Side salad']
                },
                'Low_Carb': {
                    'breakfast': ['Vegetable omelet with spinach, mushrooms, and cheese', 'Bacon or turkey sausage'],
                    'lunch': ['Cobb salad with grilled chicken, bacon, avocado, eggs, and blue cheese dressing'],
                    'dinner': ['Zucchini noodles (zoodles) with marinara sauce and turkey meatballs', 'Sautéed spinach']
                },
                'Low_Fat': {
                    'breakfast': ['Greek yogurt parfait with low-fat yogurt, fresh berries, and granola'],
                    'lunch': [
                        'Turkey and veggie wrap with whole grain tortilla, lettuce, tomato, cucumber, and mustard'],
                    'dinner': [
                        'Grilled white fish with steamed brown rice and stir-fried vegetables in a light soy sauce']
                }

            }

            # Print food suggestions for each meal
            print("Breakfast:")
            dietdata = ""
            for item in diet_suggestions[predicted_diet]['breakfast']:
                dietdata = dietdata + item

            print("\nLunch:")
            for item in diet_suggestions[predicted_diet]['lunch']:
                dietdata = dietdata + item

            print("\nDinner:")
            for item in diet_suggestions[predicted_diet]['dinner']:
                dietdata = dietdata + item

            request.session['dietdata'] = dietdata

        # Example: Predict diet type for a new person and suggest meals
        age = int(request.POST.get('age'))
        # return HttpResponse(request.POST.get('weight'))
        height = int(request.POST.get('height'))
        weight = int(request.POST.get('weight'))
        hours = int(request.POST.get('hours'))

        new_person = {'Age': age, 'Weight': weight, 'Height': height, 'Exercise_Hours': hours}
        new_df = pd.DataFrame([new_person])

        predicted_diet_probabilities = model.predict_proba(new_df)[0]
        predicted_diet = ['Balanced', 'Low_Carb', 'Low_Fat'][predicted_diet_probabilities.argmax()]

        # print("Predicted Diet Type:", predicted_diet)
        # print("\nMeal Suggestions:")
        suggest_meals(predicted_diet)
        return redirect('/trainer/dietassign')
    else:
        return HttpResponse("<script>alert('Authentication Required..');window.location='/login/';</script>")
