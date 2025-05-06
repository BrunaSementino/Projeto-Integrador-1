from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    categoria = models.CharField(max_length=50)
    quantidade = models.PositiveIntegerField(default=0)
    validade = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    estoque_minimo =  models.PositiveIntegerField(default=10)
    

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.produto.nome} ({self.quantidade})"
