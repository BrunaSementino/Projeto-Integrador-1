from django.contrib import admin
from .models import Produto, Movimentacao

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'quantidade', 'validade', 'criado_em']
    search_fields = ['nome', 'categoria']

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'tipo', 'quantidade', 'data', 'usuario']
    list_filter = ['tipo', 'data']
    search_fields = ['produto__nome', 'usuario__username']
