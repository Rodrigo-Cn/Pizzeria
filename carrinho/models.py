from django.db import models
from pizza.models import Pizza
from usuario.models import CustomUser

class Carrinho(models.Model):
    valorTotal = models.FloatField(default=0)
    quantidadeTotal = models.IntegerField(default=0)
    pizzas = models.ManyToManyField(Pizza)
    
    usuario = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )





