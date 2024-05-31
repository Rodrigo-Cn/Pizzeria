from django.db import models
from pizza.models import Pizza

class Carrinho(models.Model):
    valorTotal = models.FloatField()
    quantidadeTotal = models.IntegerField()

class ItemDeCarrinho(models.Model):
    quantidadeParcial = models.IntegerField()
    valorParcial = models.FloatField()

    carrinho = models.ForeignKey(
        Carrinho,
        on_delete=models.PROTECT,
        blank=False
    )

    pizza = models.OneToOneField(
        Pizza,
        on_delete=models.PROTECT,
        primary_key=True,
    )



