from django.forms import ModelForm
from .models import ItemDeCarrinho

class ItemDeCarrinhoForm(ModelForm):
    class Meta():
        model = ItemDeCarrinho
        fields = ['quantidade']