from django.db import models

class Caixa(models.Model):
    vendas_diarias = models.IntegerField(default=0)
    lucro_diario = models.FloatField(default=0)
    vendas_totais = models.IntegerField(default=0)
    lucro_total =  models.FloatField(default=0)

    def __str__(self):
        return "Caixa Principal"