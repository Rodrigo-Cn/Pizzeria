from django.db import models

class Pizza(models.Model):
    sabor = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=255)
    preco = models.FloatField()
    tamanho = models.CharField(max_length=100)





