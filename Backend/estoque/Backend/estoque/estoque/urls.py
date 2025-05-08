from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('movimentar/', views.registrar_movimentacao, name='registrar_movimentacao'),
    path('exportar-excel/', exportar_excel, name='exportar_excel'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),


]
