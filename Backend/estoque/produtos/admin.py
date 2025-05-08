from django.contrib import admin
from .models import Produto, Movimentacao

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'quantidade', 'estoque_minimo']
    search_fields = ['nome']

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'tipo', 'quantidade', 'data']
    list_filter = ['tipo', 'data']
    search_fields = ['produto__nome']
