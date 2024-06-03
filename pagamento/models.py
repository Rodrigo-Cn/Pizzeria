from django.db import models
from usuario.models import CustomUser, Endereco
from pizza.models import Pizza

class Pedido(models.Model):
    usuario = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    endereco = models.ForeignKey(
        Endereco,
        on_delete=models.CASCADE,
    )

    tipo_pagamento =  models.CharField(max_length=30,default="fisico")

    status = models.CharField(max_length=30)

    valorTotal = models.FloatField(default=0)

    quantidadeTotal = models.IntegerField(default=0)

    data_pedido = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f'Pedido de {self.usuario.nome} em {self.data_pedido}'

class Itenspedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens',
    )
    pizza = models.ForeignKey(
        Pizza,
        on_delete=models.CASCADE,
    )
    quantidade = models.IntegerField()

    def __str__(self):
        return f'{self.quantidade}x {self.pizza.sabor} no pedido {self.pedido.id}'
