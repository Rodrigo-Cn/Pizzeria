import os
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Pizza
from carrinho.models import Carrinho
from .forms import PizzaForm
from pagamento.models import Pedido
from usuario.models import CustomUser
from caixa.models import Caixa
import pywhatkit


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
    if request.user.is_authenticated and request.user.tipo == "A":
        user = request.user 
        pizzas = Pizza.objects.all()
        caixa = get_object_or_404(Caixa, pk=1)
        form = PizzaForm()
        template = loader.get_template("admin.html")
        context = {'user': user, 'pizzas':pizzas, 'form':form, 'caixa':caixa}
        return HttpResponse(template.render(context,request))
    
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})
    
def criarPizza(request):
    if request.user.is_authenticated and request.user.tipo == "A":
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
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})

def deletarPizza(request, pizza_id):
    if request.user.is_authenticated and request.user.tipo == "A":
        Pizza.objects.get(pk=pizza_id).delete()
        return HttpResponseRedirect('/pizza/admin/')
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})

def editarPizza(request, pizza_id):
    if request.user.is_authenticated and request.user.tipo == "A":
        user = request.user
        pizza = Pizza.objects.get(pk=pizza_id)
        template = loader.get_template("editarPizza.html")
        form = PizzaForm(request.GET, request.FILES, instance=pizza)
        context = {'user': user, 'pizza':pizza, 'form': form}
        return HttpResponse(template.render(context,request))
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})    

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

    if request.user.is_authenticated and request.user.tipo == "A":
        pizza = Pizza.objects.get(pk=pizza_id)
        form = PizzaForm(instance=pizza)
        return render(request, 'editarPizza.html', {'form':form, 'pizza':pizza})
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})    


def realizarEdicao(request, pizza_id):

    if request.user.is_authenticated and request.user.tipo == "A":
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
    
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})

def listarpedidos(request):

    if request.user.is_authenticated and request.user.tipo == "A":
        user = request.user 
        pedidos = Pedido.objects.all().order_by('-data_pedido')[:50]
        return render(request, "listapedidos.html", {'pedidos' : pedidos, 'user' : user})
    
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})

def pedidosaindo(request, id):

    if request.user.is_authenticated and request.user.tipo == "A":
        pedido = get_object_or_404(Pedido, pk=id)


        mensagem = (
            f"Olá! {pedido.usuario.nome}. o seu pedido já foi concluído. "
            f"Em breve ele chega em sua casa quentinho e saboroso!!!"
        )       
              
        pywhatkit.sendwhatmsg_instantly(f"+55" + pedido.usuario.telefone , mensagem, 10, tab_close=False)


        pedido.status = "Concluido"
        caixa = get_object_or_404(Caixa, pk=1)
        caixa.lucro_total += pedido.valorTotal
        caixa.lucro_diario += pedido.valorTotal
        caixa.vendas_diarias += pedido.quantidadeTotal
        caixa.vendas_totais += pedido.quantidadeTotal
        caixa.save()
        pedido.save()
        return redirect('listarpedidos')
    
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})

def cancelarpedido(request, id):

    if request.user.is_authenticated and request.user.tipo == "A":
        pedido = get_object_or_404(Pedido, pk=id)
        pedido.status = "Cancelado"
        pedido.save()
        return redirect('listarpedidos')
    
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})    

def listarclientes(request):

    if request.user.is_authenticated and request.user.tipo == "A":
        user = request.user
        usuario_name = request.GET.get('nome') 

        if usuario_name:
            usuarios = CustomUser.objects.filter(nome__icontains=usuario_name)
        else:
            usuarios = CustomUser.objects.all()

        usuario_paginator = Paginator(usuarios, 10)

        if not request.GET.get('page'):
            page_num = 1
        else:
            page_num = request.GET.get('page')

        page = usuario_paginator.get_page(page_num)

        return render(request, "listaclientes.html", {'usuarios' : page, 'user' : user,  'page_num' : page_num})

    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'}) 
    
def banirusuario(request, id):
    
    if request.user.is_authenticated and request.user.tipo == "A":
        usuario = get_object_or_404(CustomUser, pk=id)
        usuario.delete()
        return redirect('listarclientes')
    
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})

def zerarcaixadiario(request):

    if request.user.is_authenticated and request.user.tipo == "A":
        caixa = get_object_or_404(Caixa, pk=1)
        caixa.vendas_diarias = 0
        caixa.lucro_diario = 0
        caixa.save()
        return redirect("admin")
    
    else:
        return render(request,"login.html",{'error':'Você não está logado ou não tem permissão de administrador.'})
        