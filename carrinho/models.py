from django.db import models
from django.forms import JSONField
from pizza.models import Pizza
from usuario.models import CustomUser

class Carrinho(models.Model):
    valorTotal = models.FloatField(default=0)
    quantidadeTotal = models.IntegerField(default=0)
    
    usuario = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return "Carrinho de "+self.usuario.nome

class ItemDeCarrinho(models.Model):
    quantidade = models.IntegerField()

    pizza = models.OneToOneField(
        Pizza,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)








