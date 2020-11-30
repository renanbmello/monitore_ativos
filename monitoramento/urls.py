from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('acao.html', views.acao, name="acao"),
    path('delete/<acao_id>', views.delete, name='delete'),
]
