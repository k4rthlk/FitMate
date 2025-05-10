from django.urls import path
from . import views

urlpatterns=[
    # path('login/', views.login,name='login'),
    path('index/', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('equipmentview/', views.equipmentview, name='equipmentview'),
    path('schedule/', views.schedule, name='schedule'),
    path('workoutview/', views.workoutview, name='workoutview'),
    path('trainerview/', views.trainerview, name='trainerview'),
    path('dietview/', views.dietview, name='dietview'),
    path('applied/<id>', views.applied, name='applied'),
    path('profile/', views.profile, name='profile'),
    path('useredit/<id>', views.useredit, name='useredit'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('feedback/<id>', views.feedback, name='feedback'),

]