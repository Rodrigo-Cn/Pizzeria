from django.shortcuts import render, redirect
from carrinho.models import Carrinho
from usuario.models import Endereco
from django.contrib import messages
from .models import Pedido
from .models import Itenspedido
from carrinho.models import ItemDeCarrinho
import mercadopago
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def solicitarpagamento(request):
    if request.user.is_authenticated:
        tipopagamento = request.POST.get("tipopagamento")
        
        if tipopagamento == 'fisico':

            if request.user.is_authenticated:
                
                user = request.user
                endereco = Endereco.objects.get(usuario_id=user.id)
                carrinho = Carrinho.objects.get(usuario_id=user.id)
                context =  {'user': user, 'carrinho' : carrinho, 'carrinho' : carrinho, 'endereco' : endereco, 'tipopagamento' : "Físico"}
                return render(request, "finalizarpedido.html", context)
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
            
        carrinho.valorTotal = 0
        carrinho.quantidadeTotal = 0
        carrinho.save()
        itensDeCarrinho.delete()

        messages.success(request, 'Pedido realizado com sucesso!')
        return redirect('lista')
    
    else:
        return render(request,"login.html",{'error':'Você não está logado.'})    

def fazerpedidopix(request):

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
        
    carrinho.valorTotal = 0
    carrinho.quantidadeTotal = 0
    carrinho.save()
    itensDeCarrinho.delete()

    messages.success(request, 'Pedido realizado com sucesso!')
    return redirect('lista')


def payment_pix(request):

    user = request.user
    endereco = Endereco.objects.get(usuario_id=user.id)
    carrinho = Carrinho.objects.get(usuario_id=user.id)

    token = "TEST-868239159716244-060111-8c1b99ebdf4c0b4ca737df3337a28b3b-445985305"

    sdk = mercadopago.SDK(token)

    payment_data = {
        "transaction_amount": 20,
        "description": "Pizzaria Deliciis",
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

    payment = sdk.payment().create(payment_data)
    payment_response = payment["response"]

    return render(request, 'pagamento.html', {
        'qr_code_url': payment_response['point_of_interaction']['transaction_data']['qr_code_base64']
    })


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
                # Atualize o status do pagamento no seu banco de dados aqui
                pass

        return JsonResponse({"status": "success"})