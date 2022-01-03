from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('create', views.create, name='create'),

    path('login', views.loginpage, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logoutUser, name='logout'),

]