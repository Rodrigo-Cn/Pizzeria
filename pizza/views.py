import os
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Pizza
from carrinho.models import Carrinho
from .forms import PizzaForm


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

def admin(request):
    if request.user.is_authenticated:
        user = request.user 
        pizzas = Pizza.objects.all()
        form = PizzaForm()
       #DEPOIS QUE A MODEL DE PEDIDO TIVER SIDO FEITA, É PRECISO ADICIONÁ-LA NO CONTEXT DAQUI
        template = loader.get_template("admin.html")
        context = {'user': user, 'pizzas':pizzas, 'form':form}
        return HttpResponse(template.render(context,request))
    
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})
    
def criarPizza(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("Pizza criada com sucesso")
            return HttpResponseRedirect('/pizza/admin/')
        else:
            print("Formulário inválido:", form.errors)
    else:
        form = PizzaForm()
    return HttpResponseRedirect('/pizza/admin/')

def deletarPizza(request, pizza_id):
    Pizza.objects.get(pk=pizza_id).delete()
    return HttpResponseRedirect('/pizza/admin/')

def editarPizza(request, pizza_id):
    user = request.user
    pizza = Pizza.objects.get(pk=pizza_id)
    template = loader.get_template("editarPizza.html")
    form = PizzaForm(request.GET, request.FILES, instance=pizza)
    context = {'user': user, 'pizza':pizza, 'form': form}
    return HttpResponse(template.render(context,request))

"""
def editarPizza(request, pizza_id):
    pizza = Pizza.objects.get(pk=pizza_id)
    if request.method == 'POST':
        form = PizzaForm(request.POST, instance=pizza)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/pizza/admin/')
    else:
        form = PizzaForm(instance=pizza)
    return render(request, 'editarPizza.html', {'form':form})
"""

def editarPizza(request, pizza_id):
    pizza = Pizza.objects.get(pk=pizza_id)

    form = PizzaForm(instance=pizza)
    return render(request, 'editarPizza.html', {'form':form, 'pizza':pizza})

def realizarEdicao(request, pizza_id):
    pizza = Pizza.objects.get(pk=pizza_id)
    if request.method == 'POST':
        print("oi")
        if len(request.FILES) != 0:
            print("oi2")
            if len(pizza.imagem) > 0:
                print("o3")
                os.remove(pizza.imagem.path)
                pizza.imagem = request.FILES['imagem']
        print("========================")
        print(request.FILES)
        print("========================")
        form = PizzaForm(request.POST, request.FILES, instance=pizza)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect('/pizza/admin/')
