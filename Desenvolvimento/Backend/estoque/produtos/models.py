from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    quantidade = models.IntegerField()
    data_entrada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
