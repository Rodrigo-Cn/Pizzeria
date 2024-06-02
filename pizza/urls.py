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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
