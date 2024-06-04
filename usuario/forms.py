from django.forms import FileInput, ModelForm
from .models import CustomUser
from .models import Endereco

class UserForm(ModelForm):
    class Meta():
        model = CustomUser
        fields = ['password', 'email', 'nome', 'cpf', 'telefone']

class EnderecoForm(ModelForm):
    class Meta():
        model = Endereco
        fields = ['rua', 'bairro', 'numero']
        