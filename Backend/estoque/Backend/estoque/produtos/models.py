from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    quantidade = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    quantidade = models.PositiveIntegerField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome}"


# admin.py
from django.contrib import admin
from .models import Produto, Movimentacao

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'quantidade', 'estoque_minimo']
    search_fields = ['nome']

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'tipo', 'quantidade', 'data']
    list_filter = ['tipo', 'data']
    search_fields = ['produto__nome']


# importar_produtos.py
import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seuprojeto.settings')
django.setup()

from estoque.models import Produto

# Ajuste o caminho do arquivo Excel conforme a localização correta
df = pd.read_excel('controle epi.xlsx', sheet_name='Produtos')

for _, row in df.iterrows():
    Produto.objects.create(
        nome=row['nome'],
        descricao=row.get('descricao', ''),
        quantidade=int(row['quantidade']),
        estoque_minimo=int(row.get('estoque_minimo', 0))
    )

print("Importação concluída.")
