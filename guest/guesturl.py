from django.urls import path
from . import views

urlpatterns=[
    path('login/', views.login,name='login'),
    path('', views.index, name='gindex'),
    path('userregistration/', views.userregistration, name='userregistration'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),

]