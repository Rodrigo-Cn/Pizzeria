from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TIPO_CHOICES = (
        ('A', 'Administrador'),
        ('B', 'Usuário'),
    )

    nome = models.CharField(max_length=100, blank=True)
    cpf = models.CharField(max_length=14, blank=True, unique=True)
    telefone = models.CharField(max_length=20, blank=True, unique=True)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='B')

    def __str__(self):
        return self.nome
        

class Endereco(models.Model):

    usuario = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    rua = models.CharField(max_length=100)
    bairro =  models.CharField(max_length=80)
    numero = models.IntegerField()

    def __str__(self):
        return f'Endereço de {self.usuario.nome}'
        

    

    