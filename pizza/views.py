from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse
from .models import Pizza


def listaSabores(request):
    if request.user.is_authenticated:
        user = request.user
        pizzas = Pizza.objects.all()
        template = loader.get_template("opcoes.html")
        context = { 'pizzas': pizzas, 'user': user}
        return HttpResponse(template.render(context,request))
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})