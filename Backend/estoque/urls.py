from django.urls import path
from . import views

app_name = 'estoque'  # <-- isso ativa o namespace 'estoque'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastrar/', views.cadastrar_produto, name='cadastrar'),
    path('retirada/', views.solicitar_retirada, name='retirada'),
    path('retiradas/', views.listar_retiradas, name='listar_retiradas'),
    path('exportar/', views.exportar, name='exportar'),
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('registrar_movimentacao/', views.registrar_movimentacao, name='registrar_movimentacao'),
    path('dashboard/', views.dashboard, name='dashboard')

    
]
