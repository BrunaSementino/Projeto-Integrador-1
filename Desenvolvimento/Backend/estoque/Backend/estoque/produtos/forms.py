from django import forms
from .models import Produto, EntradaEstoque, SaidaEstoque


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'

class EntradaEstoqueForm(forms.ModelForm):
    class Meta:
        model = EntradaEstoque
        fields = ['produto', 'quantidade']

class SaidaEstoqueForm(forms.ModelForm):
    class Meta:
        model = SaidaEstoque
        fields = ['produto', 'quantidade', 'destino']
