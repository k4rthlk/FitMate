from django.urls import path
from . import views

urlpatterns=[
    path('trainerindex/', views.index, name='trainerindex'),
    path('logout/', views.logout, name='logout'),
    path('workoutreg/', views.workoutreg, name='workoutreg'),
    path('workoutedit/<id>', views.workoutedit, name='workoutedit'),
    path('workoutdelete/<id>', views.workoutdelete, name='workoutdelete'),
    path('workoutview/', views.workoutview, name='workoutview'),
    path('planreq/', views.planreq, name='planreq'),
    path('requestview/', views.requestview, name='requestview'),
    path('planconfirm/<id>', views.planconfirm, name='planconfirm'),
    path('requestreject/<id>', views.requestreject, name='requestreject'),
    path('timereq/', views.timereq, name='timereq'),
    path('timereqview/', views.timereqview, name='timereqview'),
    path('timeconfirm/<id>', views.timeconfirm, name='timeconfirm'),
    path('timereject/<id>', views.timereject, name='timereject'),
    path('userview/', views.userview, name='userview'),
    path('dietassign/', views.dietassign, name='dietassign'),
    path('dietassignedview/', views.dietassignedview, name='dietassignedview'),
    path('timeassignedview/', views.timeassignedview, name='timeassignedview'),
    path('filldietassign/', views.filldietassign, name='filldietassign'),
    path('predictdiet/', views.predictdiet, name='predictdiet'),

]