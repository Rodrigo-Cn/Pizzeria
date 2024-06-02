from django.urls import path
from . import views

urlpatterns = [
    path("adicionar/<int:pizza_id>/<int:user_id>/", views.adicionarNoCarrinho, name="adicionarNoCarrinho"),
    path("abrirCarrinho/<int:user_id>/", views.abrirCarrinho, name="abrirCarrinho"),
    path("deletarItemDeCarrinho/<int:item_id>/<int:user_id>", views.deletarItemDeCarrinho, name="deletarItemDeCarrinho"),

]