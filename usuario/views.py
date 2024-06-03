from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse

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
