from django.shortcuts import render
from django.db.models import Sum, F
from .models import Produto, Movimentacao
from datetime import datetime

def dashboard(request):
    # Filtros recebidos do formulário GET
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    tipo = request.GET.get('tipo')

    # Monta o queryset base
    movimentos = Movimentacao.objects.all()

    # Filtro por tipo
    if tipo in ['E', 'S']:
        movimentos = movimentos.filter(tipo=tipo)

    # Filtro por data
    if data_inicio:
        movimentos = movimentos.filter(data__gte=data_inicio)
    if data_fim:
        movimentos = movimentos.filter(data__lte=data_fim)

    # Calcula totais com base nos filtros
    entradas = movimentos.filter(tipo='E').aggregate(Sum('quantidade'))['quantidade__sum'] or 0
    saidas = movimentos.filter(tipo='S').aggregate(Sum('quantidade'))['quantidade__sum'] or 0

    produtos_movimentados = (
        movimentos.values('produto__nome')
        .annotate(total=Sum('quantidade'))
        .order_by('-total')[:5]
    )

    produtos_criticos = Produto.objects.filter(quantidade__lte=F('estoque_minimo'))

    context = {
        'entradas': entradas,
        'saidas': saidas,
        'produtos_movimentados': produtos_movimentados,
        'produtos_criticos': produtos_criticos,
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'tipo': tipo,
        }
    }

    return render(request, 'estoque/dashboard.html', context)
