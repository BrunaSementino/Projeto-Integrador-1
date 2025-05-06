from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.listar_produtos, name='listar_produtos'),
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('saida/', views.registrar_saida, name='registrar_saida'),
        path('historico/', views.historico_movimentacoes, name='historico_movimentacoes'),
path('relatorio/pdf/', views.gerar_pdf_movimentacoes, name='gerar_pdf_movimentacoes'),
path('relatorio/excel/', views.exportar_excel_movimentacoes, name='exportar_excel_movimentacoes'),

]
