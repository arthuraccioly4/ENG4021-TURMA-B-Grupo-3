from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from SaveMarket.Produtos.models import Produto, MercadoParceiro


def home(request):
    produtos = Produto.objects.filter(validade__gte=timezone.now().date())
    mercados = MercadoParceiro.objects.all()

    # Busca
    q = request.GET.get('q', '')
    if q:
        produtos = produtos.filter(titulo__icontains=q)

    # Ordenação
    sort = request.GET.get('sort', 'validade')
    if sort == 'desconto':
        produtos = sorted(produtos, key=lambda p: p.percentual_desconto, reverse=True)
    elif sort == 'preco':
        produtos = produtos.order_by('preco_desconto')
    else:
        produtos = produtos.order_by('validade')

    return render(request, 'home.html', {
        'produtos': produtos,
        'mercados': mercados,
    })


def produto_view(request, pk=None):
    if pk:
        produto = get_object_or_404(Produto, pk=pk)
        return render(request, 'produto.html', {'produto': produto})
    return render(request, 'produto.html')


def mercado_view(request, pk):
    mercado = get_object_or_404(MercadoParceiro, pk=pk)
    produtos = mercado.produtos.all().order_by('validade')
    return render(request, 'mercado.html', {'mercado': mercado, 'produtos': produtos})


@staff_member_required
def admin_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})


def registro_view(request):
    mensagem = ''
    if request.method == 'POST':
        nome  = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        if User.objects.filter(email=email).exists():
            mensagem = 'E-mail já cadastrado.'
        else:
            User.objects.create_user(username=email, email=email,
                                     password=senha, first_name=nome)
            return redirect('login')
    return render(request, 'registro.html', {'mensagem': mensagem})


def login_view(request):
    mensagem = ''
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            username = None
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        else:
            mensagem = 'E-mail ou senha incorretos.'
    return render(request, 'login.html', {'mensagem': mensagem})


@login_required
def perfil_view(request):
    return render(request, 'perfil.html')

@login_required
def carrinho_view(request):
    carrinho = request.session.get('carrinho', {})
 
    itens = []
    total_original = 0
    total_com_desconto = 0
 
    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, pk=produto_id)
        subtotal_original = produto.preco_original * quantidade
        subtotal_desconto = produto.preco_desconto * quantidade
 
        itens.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal_original': subtotal_original,
            'subtotal_desconto': subtotal_desconto,
        })
 
        total_original += subtotal_original
        total_com_desconto += subtotal_desconto
 
    economia = total_original - total_com_desconto
 
    return render(request, 'carrinho.html', {
        'itens': itens,
        'total_original': total_original,
        'total_com_desconto': total_com_desconto,
        'economia': economia,
    })
 
 
@login_required
def adicionar_carrinho(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    carrinho = request.session.get('carrinho', {})
 
    pk_str = str(pk)
    carrinho[pk_str] = carrinho.get(pk_str, 0) + 1
 
    request.session['carrinho'] = carrinho
    messages.success(request, f'"{produto.titulo}" adicionado ao carrinho.')
    return redirect('home')
 
 
@login_required
def remover_carrinho(request, pk):
    carrinho = request.session.get('carrinho', {})
    pk_str = str(pk)
 
    if pk_str in carrinho:
        del carrinho[pk_str]
        request.session['carrinho'] = carrinho
 
    return redirect('carrinho')
 
 
@login_required
def atualizar_carrinho(request, pk):
    if request.method == 'POST':
        carrinho = request.session.get('carrinho', {})
        pk_str = str(pk)
        nova_quantidade = int(request.POST.get('quantidade', 1))
 
        if nova_quantidade <= 0:
            carrinho.pop(pk_str, None)
        else:
            carrinho[pk_str] = nova_quantidade
 
        request.session['carrinho'] = carrinho
 
    return redirect('carrinho')