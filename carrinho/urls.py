from django.urls import path
from . import views

urlpatterns = [
    path("adicionar/<int:pizza_id>/<int:user_id>/", views.adicionarNoCarrinho, name="adicionarNoCarrinho"),
]