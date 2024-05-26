from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('cadastrar/', views.cadastrar, name='cadastro'),
    path('deliciis/', views.deliciis, name='deliciis'),
]
