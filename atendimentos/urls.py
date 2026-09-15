from django.urls import path
from . import views

urlpatterns = [
    path('', views.hoje, name='hoje'),
    path('registrar/<int:grupo_id>/', views.registrar, name='registrar'),
    path('extra/', views.extra, name='extra'),
    path('folha/', views.folha, name='folha'),
    path('folha/excel/', views.excel, name='excel'),
    path('enviar/', views.enviar, name='enviar'),
]
