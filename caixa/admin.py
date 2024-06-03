from django.contrib import admin
from .models import Caixa

class CaixaAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendas_diarias', 'lucro_diario', 'vendas_totais', 'lucro_total')

admin.site.register(Caixa, CaixaAdmin)
