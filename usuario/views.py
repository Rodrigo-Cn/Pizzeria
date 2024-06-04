from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse
from pagamento.models import Pedido
from .forms import EnderecoForm, UserForm
from .models import Endereco

CustomUser = get_user_model()

def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('/pizza/admin/')
            else:
                login(request, user)
                return redirect('/pizza/listasabores/')
        else:
            return render(request, 'login.html', {'error': "Username ou senha incorretos!"})

    else:
        return render(request, 'login.html')


def cadastrar(request):
    if request.user.is_authenticated and request.user.tipo == 'B':
        return redirect('lista')
    elif request.user.is_authenticated and request.user.tipo == 'A':
        return redirect('admin')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha1')
            cpf = request.POST.get('cpf')
            telefone = request.POST.get('telefone')
            
            if CustomUser.objects.filter(username=username).exists():
                erro = "Username já existe"
                return render(request, 'home.html', {'erro': erro})
            elif CustomUser.objects.filter(email=email).exists():
                erro = "Email já foi cadastrado"
                return render(request, 'home.html', {'erro': erro})
            elif CustomUser.objects.filter(cpf=cpf).exists():
                erro = "CPF já foi cadastrado"
                return render(request, 'home.html', {'erro': erro})
            elif CustomUser.objects.filter(telefone=telefone).exists():
                erro = "Telefone já foi cadastrado"
                return render(request, 'home.html', {'erro': erro, 'ancora': 'cadastro'})
            else:
                user = CustomUser(
                    username=username,
                    nome=nome,
                    email=email,
                    cpf=cpf,
                    telefone=telefone,
                )
                user.set_password(senha)
                user.save()
                messages.success(request, 'Usuário criado com sucesso! Faça login para continuar.')
                return redirect('login')
        else:
            return render(request, 'cadastrar.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def usernavpage(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'userpage.html', {'user':user})
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})
    

def meuspedidos(request):
    if request.user.is_authenticated:
        user = request.user
        pedidos =  Pedido.objects.filter(usuario=user).order_by('-data_pedido')
        return render(request, 'meuspedidos.html', {'user':user, 'pedidos':pedidos})
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})

def endereco(request):
    if request.user.is_authenticated:
        user = request.user
        if Endereco.objects.filter(usuario_id=user.id):
            endereco = Endereco.objects.get(usuario_id=user.id)
            form = EnderecoForm(instance=endereco)
        
        return render(request, 'editarEndereco.html', {'user':user, 'form':form})
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})
    
def editarEndereco(request):
    if request.user.is_authenticated:
        user = request.user

        if Endereco.objects.filter(usuario_id=user.id):
            endereco = Endereco.objects.get(usuario_id=user.id)
            if request.method == 'POST':
                form = EnderecoForm(request.POST, instance=endereco)
                if form.is_valid():
                    form.save()
                    return render(request, 'userpage.html', {'user':user})
        else:
            if request.method == 'POST':
                endereco = Endereco()
                endereco.usuario = user
                form = EnderecoForm(request.POST, instance=endereco)
                if form.is_valid():
                    form.save()
                    return render(request, 'userpage.html', {'user':user})
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})

def editarperfil(request):
        
        if request.user.is_authenticated:
            user = request.user
            if request.method == 'POST':
                username = request.POST.get('username')
                nome = request.POST.get('nome')
                email = request.POST.get('email')
                senha = request.POST.get('senha1')
                cpf = request.POST.get('cpf')
                telefone = request.POST.get('telefone')
                
                if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
                    erro = "Username já existe"
                    return render(request, 'editarperfil.html', {'erro': erro})
                elif CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
                    erro = "Email já foi cadastrado"
                    return render(request, 'editarperfil.html', {'erro': erro})
                elif CustomUser.objects.filter(cpf=cpf).exclude(id=user.id).exists():
                    erro = "CPF já foi cadastrado"
                    return render(request, 'editarperfil.html', {'erro': erro})
                elif CustomUser.objects.filter(telefone=telefone).exclude(id=user.id).exists():
                    erro = "Telefone já foi cadastrado"
                    return render(request, 'editarperfil.html', {'erro': erro})
                else:
                    user.username = username
                    user.nome = nome
                    user.email = email
                    user.cpf = cpf
                    user.telefone = telefone
                    if senha:
                        user.set_password(senha)
                    user.save()
                    messages.success(request, 'Usuário editado com sucesso, faça o login para confirmar alterações.')
                return redirect('login')
            else:
                return render(request, 'editarperfil.html', {'user': user})

        else:
            return render(request, 'cadastrar.html')