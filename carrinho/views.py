from django.template import loader
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Carrinho, Pizza, ItemDeCarrinho
from usuario.models import CustomUser

"""def adicionarNoCarrinho(request, pizza_id, user_id):
    carrinho = Carrinho.objects.get(usuario_id=user_id)
    pizza = Pizza.objects.get(pk=pizza_id)

    definir_dicionario_das_pizzas_do_carrinho_e_suas_quantidades(user_id)

    carrinho.valorTotal += pizza.preco
    carrinho.quantidadeTotal = carrinho.retorna_quantidade_total()
    carrinho.pizzas.add(pizza)

    carrinho.save()

    return redirect('/pizza/listasabores')

def abrirCarrinho(request, user_id):
    carrinho = Carrinho.objects.get(usuario_id=user_id)
    user = CustomUser.objects.get(pk=user_id)
    pizzasDoCarrinho = carrinho.pizzas.all()

    template = loader.get_template("carrinho.html")
    context = { 'pizzasDoCarrinho': pizzasDoCarrinho, 'user': user, 'carrinho':carrinho}
    return HttpResponse(template.render(context,request))

def definir_dicionario_das_pizzas_do_carrinho_e_suas_quantidades(user_id):
    carrinho = Carrinho.objects.get(usuario_id=user_id)
    pizzasDoCarrinho = carrinho.pizzas.all()

    for pizzaDoCarrinho in pizzasDoCarrinho:
        carrinho.adicionar_quantidade(pizzaDoCarrinho, 1)

    return True
"""
 
def adicionarNoCarrinho(request, pizza_id, user_id):
    itemNovo = ItemDeCarrinho()
    carrinho = Carrinho.objects.get(pk=user_id)
    itemNovo.pizza = Pizza.objects.get(pk=pizza_id)

    itensDeCarrinho = []
    if ItemDeCarrinho.objects.filter(carrinho_id=user_id).exists():
        itensDeCarrinho = ItemDeCarrinho.objects.filter(carrinho_id=user_id)
    
    for itemDeCarrinho in itensDeCarrinho:
        if itemDeCarrinho.pizza.id == itemNovo.pizza.id:
            itemDeCarrinho.quantidade += 1
            itemDeCarrinho.save()

            carrinho.valorTotal += itemDeCarrinho.pizza.preco
            carrinho.quantidadeTotal = define_quantidade_total(user_id)
            carrinho.save()
            return redirect('/pizza/listasabores')
    
    itemNovo.quantidade = 1
    itemNovo.carrinho = carrinho
    carrinho.valorTotal += itemNovo.pizza.preco
    carrinho.quantidadeTotal = define_quantidade_total(user_id)
    itemNovo.save()
    carrinho.save()
    return redirect('/pizza/listasabores')

def define_quantidade_total(user_id):
    itensDeCarrinho = []
    cont = 0

    if ItemDeCarrinho.objects.filter(carrinho_id=user_id).exists():
        itensDeCarrinho = ItemDeCarrinho.objects.filter(carrinho_id=user_id)
    
    for itemDeCarrinho in itensDeCarrinho:
        cont += itemDeCarrinho.quantidade
    
    return cont


def abrirCarrinho(request, user_id):
    carrinho = Carrinho.objects.get(usuario_id=user_id)
    user = CustomUser.objects.get(pk=user_id)
    if ItemDeCarrinho.objects.filter(carrinho_id=user_id).exists():
        itensDeCarrinho = ItemDeCarrinho.objects.filter(carrinho_id=user_id)

    template = loader.get_template("carrinho.html")
    context = { 'itensDeCarrinho': itensDeCarrinho, 'user': user, 'carrinho':carrinho}
    return HttpResponse(template.render(context,request))


    
    


