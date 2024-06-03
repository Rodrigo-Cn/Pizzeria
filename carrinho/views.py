from django.template import loader
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Carrinho, Pizza, ItemDeCarrinho
from usuario.models import CustomUser

def adicionarNoCarrinho(request, pizza_id, user_id):
    print("oioioioioioioioioinasdasdasd")
    itemNovo = ItemDeCarrinho()
    carrinho = Carrinho.objects.get(pk=user_id)
    itemNovo.pizza = Pizza.objects.get(pk=pizza_id)

    itensDeCarrinho = []
    
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
    itemNovo.save()

    carrinho.valorTotal += itemNovo.pizza.preco
    carrinho.quantidadeTotal = define_quantidade_total(user_id)
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
    else:
        template = loader.get_template("carrinho.html")
        context = {'user': user, 'carrinho':carrinho}

    
    return HttpResponse(template.render(context,request))


def deletarItemDeCarrinho(request, item_id, user_id):
    itemDeletado = ItemDeCarrinho.objects.get(pizza_id=item_id)
    itemDeletado.quantidade -= 1
    precoDeletado = itemDeletado.pizza.preco

    if itemDeletado.quantidade == 0:
        ItemDeCarrinho.objects.get(pizza_id=item_id).delete()
    else:
        itemDeletado.save()

    carrinho = Carrinho.objects.get(pk=user_id)
    carrinho.valorTotal -= precoDeletado 
    carrinho.quantidadeTotal = define_quantidade_total(user_id)
    carrinho.save()

    return HttpResponseRedirect(reverse('abrirCarrinho', args=[user_id]))




    
    


