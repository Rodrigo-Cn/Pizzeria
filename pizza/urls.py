from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('listasabores/', views.listaSabores, name='lista'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
