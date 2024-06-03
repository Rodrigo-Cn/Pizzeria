from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('listasabores/', views.listaSabores, name='lista'),
    path('admin/', views.admin, name='admin'),
    path('detalhes/<int:id>/', views.detalhes, name='detalhes'),
    path('criarPizza/', views.criarPizza, name='criarPizza'),
    path('deletarPizza/<int:pizza_id>/', views.deletarPizza, name='deletarPizza'),
    path('editarPizza/<int:pizza_id>/', views.editarPizza, name='editarPizza'),
    path('realizarEdicao/<int:pizza_id>/', views.realizarEdicao, name='realizarEdicao'),
    path('listarpedidos/', views.listarpedidos, name='listarpedidos'),
    path('listarclientes/', views.listarclientes, name='listarclientes'),
    path('banirusuario/<int:id>', views.banirusuario, name='banirusuario'),
    path('pedidosaindo/<int:id>/', views.pedidosaindo, name='pedidosaindo'),
    path('cancelarpedido/<int:id>/', views.cancelarpedido, name='cancelarpedido'),
    path('zerarcaixadiario/', views.zerarcaixadiario, name='zerarcaixadiario'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
