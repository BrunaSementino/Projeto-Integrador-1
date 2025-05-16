from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, F
from .models import Produto, Retirada
from .forms import ProdutoForm, RetiradaForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SolicitacaoForm
from .models import Solicitacao, Produto
from django.contrib import messages
import pandas as pd

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'estoque/login.html', {'erro': 'Credenciais inválidas'})
    return render(request, 'estoque/login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('estoque:login')

# Dashboard (simples)
def dashboard(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/dashboard.html', {'produtos': produtos})

# Cadastro de produto
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProdutoForm()
    return render(request, 'estoque/cadastro.html', {'form': form})

# Solicitação de retirada
def solicitar_retirada(request):
    if request.method == 'POST':
        form = RetiradaForm(request.POST)
        if form.is_valid():
            retirada = form.save(commit=False)
            produto = retirada.produto
            if retirada.quantidade <= produto.estoque_fisico:
                produto.estoque_fisico -= retirada.quantidade
                produto.save()
                retirada.save()
                return redirect('listar_retiradas')
            else:
                form.add_error('quantidade', 'Quantidade indisponível em estoque.')
    else:
        form = RetiradaForm()
    return render(request, 'estoque/solicitar_retirada.html', {'form': form})

# Listagem de retiradas
def listar_retiradas(request):
    retiradas = Retirada.objects.select_related('produto').all().order_by('-data')
    return render(request, 'estoque/listar_retirada.html', {'retiradas': retiradas})

# Exportar para Excel
def exportar_excel(request):
    produtos = Produto.objects.all()
    dados = [{
        'Produto': p.nome,
        'Estoque': p.estoque_fisico,
        'Preço Unitário': float(p.preco_unitario)
    } for p in produtos]

    df = pd.DataFrame(dados)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="estoque.xlsx"'
    df.to_excel(response, index=False)

    return response

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/listar_produtos.html', {'produtos': produtos})

def registrar_movimentacao(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        tipo = request.POST.get('tipo')  # 'E' ou 'S'
        quantidade = int(request.POST.get('quantidade', 0))

        try:
            produto = Produto.objects.get(id=produto_id)
            if tipo == 'E':
                produto.estoque_fisico += quantidade
            elif tipo == 'S':
                if quantidade > produto.estoque_fisico:
                    messages.error(request, 'Quantidade insuficiente em estoque.')
                    return redirect('estoque:dashboard')
                produto.estoque_fisico -= quantidade
            produto.save()
            messages.success(request, 'Movimentação registrada com sucesso.')
        except Produto.DoesNotExist:
            messages.error(request, 'Produto não encontrado.')

    return redirect('estoque:dashboard')

def importar_planilha():
    df = pd.read_excel('controle epi.xlsx')  # ajuste se estiver em outra pasta
    for _, row in df.iterrows():
        Produto.objects.create(
            nome=row['Nome'],
            estoque_fisico=row['Estoque'],
            estoque_minimo=row['Estoque Minimo'],
            preco_unitario=row['Preço Unitario']
        )
    print("Importação concluída!")

def dashboard(request):
    # lógica aqui
    return render(request, 'estoque/dashboard.html')

def exportar(request):
    return HttpResponse("Exportar em desenvolvimento.")

@login_required
def solicitar_retirada(request):
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.usuario = request.user
            solicitacao.save()
            messages.success(request, f"Solicitação criada com código OS-{solicitacao.codigo_os}")
            return redirect('estoque:dashboard')
    else:
        form = SolicitacaoForm()
    return render(request, 'estoque/solicitar_retirada.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def listar_retiradas(request):
    solicitacoes = Solicitacao.objects.all().order_by('-data_solicitacao')
    return render(request, 'estoque/listar_retiradas.html', {'solicitacoes': solicitacoes})

@user_passes_test(lambda u: u.is_superuser)
def aprovar_retirada(request, pk):
    solicitacao = get_object_or_404(Solicitacao, pk=pk)
    if solicitacao.status == 'PENDENTE':
        produto = solicitacao.produto
        if produto.estoque_fisico >= solicitacao.quantidade:
            produto.estoque_fisico -= solicitacao.quantidade
            produto.save()
            solicitacao.status = 'APROVADA'
            solicitacao.save()
            messages.success(request, f"OS-{solicitacao.codigo_os} aprovada.")
        else:
            messages.error(request, "Estoque insuficiente.")
    return redirect('estoque:listar_retiradas')

@user_passes_test(lambda u: u.is_superuser)
def negar_retirada(request, pk):
    solicitacao = get_object_or_404(Solicitacao, pk=pk)
    if solicitacao.status == 'PENDENTE':
        solicitacao.status = 'NEGADA'
        solicitacao.save()
        messages.info(request, f"OS-{solicitacao.codigo_os} foi negada.")
    return redirect('estoque:listar_retiradas')