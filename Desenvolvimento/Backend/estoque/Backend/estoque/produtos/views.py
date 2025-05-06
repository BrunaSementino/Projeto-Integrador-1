from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import Movimentacao

def gerar_pdf_movimentacoes(request):
    movimentacoes = Movimentacao.objects.all().order_by('-data')
    template_path = 'estoque/pdf_movimentacoes.html'
    context = {'movimentacoes': movimentacoes}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_movimentacoes.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response
import openpyxl
from django.http import HttpResponse
from .models import Movimentacao

def exportar_excel_movimentacoes(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Movimentações'

    # Cabeçalhos
    ws.append(['Produto', 'Tipo', 'Quantidade', 'Data', 'Usuário'])

    # Dados
    movimentacoes = Movimentacao.objects.all().order_by('-data')
    for mov in movimentacoes:
        ws.append([
            mov.produto.nome,
            'Entrada' if mov.tipo == 'entrada' else 'Saída',
            mov.quantidade,
            mov.data.strftime('%d/%m/%Y %H:%M'),
            mov.usuario.username
        ])

    # Resposta HTTP com o arquivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=relatorio_movimentacoes.xlsx'
    wb.save(response)
    return response
from django.db.models import Count, Sum
from .models import Movimentacao, Produto

def dashboard(request):
    entradas = Movimentacao.objects.filter(tipo='entrada').count()
    saidas = Movimentacao.objects.filter(tipo='saida').count()

    produtos_movimentados = (
        Movimentacao.objects
        .values('produto__nome')
        .annotate(total=Sum('quantidade'))
        .order_by('-total')[:5]
    )

    context = {
        'entradas': entradas,
        'saidas': saidas,
        'produtos_movimentados': produtos_movimentados
    }

    return render(request, 'estoque/dashboard.html', context)
