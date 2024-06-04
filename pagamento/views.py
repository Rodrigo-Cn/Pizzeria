from django.shortcuts import render, redirect
from carrinho.models import Carrinho
from usuario.models import Endereco
from django.contrib import messages
from .models import Pedido, CustomUser
from .models import Itenspedido
from carrinho.models import ItemDeCarrinho
import mercadopago
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pywhatkit
import uuid
from usuario.forms import EnderecoForm

def solicitarpagamento(request):
    if request.user.is_authenticated:
        tipopagamento = request.POST.get("tipopagamento")

        if tipopagamento == 'fisico':

            if request.user.is_authenticated:
                
                user = request.user
                
                if Endereco.objects.filter(usuario_id=user.id):
                    endereco = Endereco.objects.get(usuario_id=user.id)
                    carrinho = Carrinho.objects.get(usuario_id=user.id)
                    context =  {'user': user, 'carrinho' : carrinho, 'carrinho' : carrinho, 'endereco' : endereco, 'tipopagamento' : "Físico"}
                    return render(request, "finalizarpedido.html", context)
                else:
                    form = EnderecoForm()
                    msg = "Por favor, insira seu endereço antes de confirmar seu pedido! Depois de inserir, retorne para a tela do carrinho."
                    return render(request, "editarEndereco.html", {'user':user, 'form':form, 'msg':msg})
            else:
                return render(request,"login.html",{'error':'Você não está logado.'})
        else:
            if request.user.is_authenticated:
                return redirect('payment_pix')

            else:
                return render(request,"login.html",{'error':'Você não está logado.'})
    
def fazerpedido(request):
    if request.user.is_authenticated:

        user = request.user
        endereco = Endereco.objects.get(usuario_id=user.id)
        carrinho = Carrinho.objects.get(usuario_id=user.id)
        itensDeCarrinho = ItemDeCarrinho.objects.filter(carrinho_id=user.id)
        
        pedido = Pedido.objects.create(
            usuario=user,
            endereco=endereco,
            tipo_pagamento='Físico',
            status='Pendente',
            valorTotal=carrinho.valorTotal,
            quantidadeTotal=carrinho.quantidadeTotal
        )

        for item in itensDeCarrinho:
            Itenspedido.objects.create(
                    pedido=pedido,
                    pizza=item.pizza,
                    quantidade=item.quantidade
                )
        
        lista_itens = ""
        admin = CustomUser.objects.get(pk=1)
        numero_do_dono = admin.telefone

        for item in itensDeCarrinho:
            lista_itens += f"- Pizza: {item.pizza.sabor}\n"
            lista_itens += f"- Pizza: {item.pizza.tamanho}\n"
            lista_itens += f"- Quantidade: {item.quantidade}\n"
            lista_itens += "--------------------------------\n"
    
        mensagem = (
            f"Olá! Meu nome é {user.nome}. Eu acabei de realizar um pedido em sua loja. "
            f"Os itens que pedi foram estes: \n{lista_itens}"
            f"O valor total do pedido foi: {carrinho.valorTotal}\n"
            f"Faça a entrega na Rua: {endereco.rua}, Bairro: {endereco.bairro}, Número: {endereco.numero}."
            f"Aguardo a confirmação do pedido : )"
        )       
              
        pywhatkit.sendwhatmsg_instantly(f"+5577998230506" , mensagem, 10, tab_close=False)
                
        carrinho.valorTotal = 0
        carrinho.quantidadeTotal = 0
        carrinho.save()
        itensDeCarrinho.delete()

        messages.success(request, 'Pedido realizado com sucesso!')
        return redirect('lista')
    
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})    

def fazerpedidopix(request):

    if request.user.is_authenticated:

        user = request.user
        endereco = Endereco.objects.get(usuario_id=user.id)
        carrinho = Carrinho.objects.get(usuario_id=user.id)
        itensDeCarrinho = ItemDeCarrinho.objects.filter(carrinho_id=user.id)

        pedido = Pedido.objects.create(
            usuario=user,
            endereco=endereco,
            tipo_pagamento='Pix',
            status='Pendente',
            valorTotal=carrinho.valorTotal,
            quantidadeTotal=carrinho.quantidadeTotal
        )

        for item in itensDeCarrinho:
            Itenspedido.objects.create(
                    pedido=pedido,
                    pizza=item.pizza,
                    quantidade=item.quantidade
                )   
            
        carrinho.valorTotal = 0
        carrinho.quantidadeTotal = 0
        carrinho.save()
        itensDeCarrinho.delete()

        messages.success(request, 'Pedido realizado com sucesso!')
        return redirect('lista')
        
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})  


def payment_pix(request):

    if request.user.is_authenticated:
        user = request.user
        endereco = Endereco.objects.get(usuario_id=user.id)
        carrinho = Carrinho.objects.get(usuario_id=user.id)

        token = "TEST-868239159716244-060111-8c1b99ebdf4c0b4ca737df3337a28b3b-445985305"
        sdk = mercadopago.SDK(token)

        idempotency_key = str(uuid.uuid4())

        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': idempotency_key
        }

        payment_data = {
            "transaction_amount": carrinho.valorTotal,
            "description": "Pizzaria Deliciis - Pedido de " + user.nome,
            "payment_method_id": "pix",
            "payer": {
                "email": user.email,
                "first_name": user.nome,
                "last_name": "Nulo",
                "identification": {
                    "type": user.cpf,
                    "number": user.telefone
                }
            }
        }

        payment_response = sdk.payment().create(payment_data, request_options)
        payment = payment_response["response"]
        link = payment['point_of_interaction']['transaction_data']['ticket_url']

        context = {
            'user': user,
            'carrinho': carrinho,
            'endereco': endereco,
            'tipopagamento': "Pix",
            'linkpix': link
        }

        return render(request, 'pagamentopix.html', context)
     
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})  


@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        token = "TEST-868239159716244-060111-8c1b99ebdf4c0b4ca737df3337a28b3b-445985305"
        event = request.json
        if event["type"] == "payment":
            payment_id = event["data"]["id"]
            sdk = mercadopago.SDK(token)
            payment_info = sdk.payment().get(payment_id)
            payment_status = payment_info["response"]["status"]

            if payment_status == 'approved':
                #Banco de Dados
                pass

        return JsonResponse({"status": "success"})