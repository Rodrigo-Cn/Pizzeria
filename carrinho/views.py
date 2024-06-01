from django.shortcuts import render
from django.http import HttpResponse
from .models import Carrinho, Pizza
from usuario.models import CustomUser

def adicionarNoCarrinho(pizza_id, user_id):
    carrinho = Carrinho.objects.get(usuario_id=user_id)

    pizza = Pizza.objects.get(pk=pizza_id)
    carrinho.valorTotal += pizza.preco
    carrinho.quantidadeTotal += 1
    
    carrinho.save()
