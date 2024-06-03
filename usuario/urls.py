from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('cadastrar/', views.cadastrar, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('usernavpage/', views.usernavpage, name='usernavpage'),
    path('meuspedidos/', views.meuspedidos, name='meuspedidos'),
]
