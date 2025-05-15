from django.db import models
from django.contrib.auth.models import User


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    estoque_fisico = models.IntegerField()
    estoque_minimo = models.IntegerField(default=0)  # ✅ Este campo precisa existir!
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


    def __str__(self):
        return self.nome

from django.contrib.auth.models import User

class Solicitacao(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADA', 'Aprovada'),
        ('NEGADA', 'Negada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    codigo_os = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"OS-{self.codigo_os} | {self.usuario.username} - {self.produto.nome}"


class Retirada(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    solicitante = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.solicitante} retirou {self.quantidade} de {self.produto.nome}'
