from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse
from .models import Pizza
from carrinho.models import Carrinho


def listaSabores(request):
    if request.user.is_authenticated:
        user = request.user
        carrinho = criarCarrinhoDoUsuario(user)
        pizzas = Pizza.objects.all()
        template = loader.get_template("opcoes.html")
        context = { 'pizzas': pizzas, 'user': user, 'carrinho':carrinho}
        return HttpResponse(template.render(context,request))
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})
    
def criarCarrinhoDoUsuario(user):
    carrinhos = Carrinho.objects.all()
    novo_carrinho = Carrinho()

    for carrinho in carrinhos:
        if carrinho.usuario:
            if carrinho.usuario.id == user.id:
                return carrinho

    novo_carrinho = Carrinho()    
    novo_carrinho.usuario = user
    novo_carrinho.save()
    return novo_carrinho