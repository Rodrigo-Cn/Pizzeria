from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views
from .views import payment_pix
from .views import payment_webhook

urlpatterns = [
    path('', views.solicitarpagamento, name='pagamento'),
    path('fazerpedido/', views.fazerpedido, name='fazerpedido'),
    path('fazerpedidopix/', views.fazerpedidopix, name='fazerpedidopix'),
    path('payment_pix/', payment_pix, name='payment_pix'),
    path('payment_webhook/', payment_webhook, name='payment_webhook'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
