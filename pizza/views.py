from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Pizza
from carrinho.models import Carrinho


def listaSabores(request):
    if request.user.is_authenticated:

        pizza_name = request.GET.get('sabor') 

        if pizza_name:
            pizzas = Pizza.objects.filter(sabor__icontains=pizza_name)
        else:
            pizzas = Pizza.objects.all()
            

        user = request.user

        pizza_paginator = Paginator(pizzas, 8)
        carrinho = criarCarrinhoDoUsuario(user)
        if request.GET.get('page'):
            page_num = request.GET.get('page')
        else:
            page_num = 1


        page = pizza_paginator.get_page(page_num)
        template = loader.get_template("opcoes.html")
        context = { 'pizzas': page, 'user': user, 'page_num' : page_num, 'carrinho' : carrinho}

        return HttpResponse(template.render(context,request))
    
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})
    
def detalhes(request, id):
    if request.user.is_authenticated:
        user = request.user
        pizza = Pizza.objects.get(id=id)
        context = { 'pizza': pizza, 'user': user}
        return render(request,"detail.html",context)
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