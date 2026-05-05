from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ItemEstoque, SaidaEstoque
from .forms import ItemEstoqueForm, SaidaEstoqueForm

@login_required
def lista_estoque(request):
    # Processa formulário de cadastro de item
    if request.method == 'POST':
        # Verifica se é cadastro de item ou saída
        if 'nome' in request.POST:  # formulário de item
            form = ItemEstoqueForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('lista_estoque')
            else:
                # Depuração: exibe erros de validação no terminal
                print("Erros no formulário de item:", form.errors)
                print("Dados recebidos:", request.POST)
        else:  # formulário de saída
            form_saida = SaidaEstoqueForm(request.POST)
            if form_saida.is_valid():
                saida = form_saida.save(commit=False)
                # Atualiza quantidade do item
                item = saida.item
                if item.quantidade_atual >= saida.quantidade:
                    item.quantidade_atual -= saida.quantidade
                    item.save()
                    saida.save()
                # Se quantidade insuficiente, talvez exibir erro
                return redirect('lista_estoque')
            else:
                # Depuração: exibe erros de validação no terminal
                print("Erros no formulário de saída:", form_saida.errors)
                print("Dados recebidos:", request.POST)
    else:
        form = ItemEstoqueForm()
        form_saida = SaidaEstoqueForm()

    itens = ItemEstoque.objects.all().order_by('nome')
    saidas = SaidaEstoque.objects.all().order_by('-data_hora')[:10]  # últimas 10
    entradas_recentes = ItemEstoque.objects.all().order_by('-data_criacao')[:10]

    context = {
        'itens': itens,
        'form': form,
        'form_saida': form_saida,
        'saidas': saidas,
        'entradas_recentes': entradas_recentes,
    }
    return render(request, 'estoque.html', context)
