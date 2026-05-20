from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from django.utils import timezone
from .models import ItemEstoque, SaidaEstoque, Categoria, OrdemServico
from .forms import ItemEstoqueForm, SaidaEstoqueForm, OrdemServicoForm, OsFinishForm, OsReopenForm

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
    total_geral = ItemEstoque.objects.aggregate(total=Sum(F('quantidade_atual') * F('preco_unitario')))['total'] or 0

    context = {
        'itens': itens,
        'form': form,
        'form_saida': form_saida,
        'saidas': saidas,
        'entradas_recentes': entradas_recentes,
        'total_geral': total_geral,
    }
    return render(request, 'estoque.html', context)


@login_required
def editar_item(request, item_id):
    item = get_object_or_404(ItemEstoque, id=item_id)
    if request.method == 'POST':
        form = ItemEstoqueForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item atualizado com sucesso.')
            return redirect('lista_estoque')
        else:
            messages.error(request, 'Erro ao atualizar item. Verifique os dados.')
            return redirect('lista_estoque')
    return redirect('lista_estoque')


@login_required
def excluir_item(request, item_id):
    item = get_object_or_404(ItemEstoque, id=item_id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item excluído com sucesso.')
        return redirect('lista_estoque')
    return redirect('lista_estoque')


@login_required
def historico_item(request, item_id):
    item = get_object_or_404(ItemEstoque, id=item_id)
    saidas = SaidaEstoque.objects.filter(item=item).order_by('-data_hora')
    entradas = [item]  # simplificado
    context = {
        'item': item,
        'saidas': saidas,
        'entradas': entradas,
    }
    return render(request, 'historico_item.html', context)


@login_required
def os_list(request):
    ordens = OrdemServico.objects.all().order_by('-data_criacao')
    context = {'ordens': ordens}
    return render(request, 'inventory/os_list.html', context)


def debitar_estoque(ordem):
    """Subtrai 1 da quantidade de cada item associado à OS, se ainda não foi efetuada."""
    if not ordem.estoque_debitado:
        for item in ordem.itens.all():
            if item.quantidade_atual > 0:
                item.quantidade_atual -= 1
                item.save()
        ordem.estoque_debitado = True
        ordem.save(update_fields=['estoque_debitado'])

def reverter_baixa(ordem):
    """Reverte a baixa de estoque (incrementa 1 em cada item)."""
    if ordem.estoque_debitado:
        for item in ordem.itens.all():
            item.quantidade_atual += 1
            item.save()
        ordem.estoque_debitado = False
        ordem.save(update_fields=['estoque_debitado'])


@login_required
def os_create(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            ordem = form.save(commit=False)
            ordem.save()
            form.save_m2m()  # salva ManyToMany
            debitar_estoque(ordem)
            messages.success(request, 'Ordem de Serviço criada com sucesso.')
            return redirect('os_list')
        else:
            messages.error(request, 'Erro ao criar OS. Verifique os dados.')
    else:
        form = OrdemServicoForm()
    context = {'form': form}
    return render(request, 'inventory/os_form.html', context)


@login_required
def os_edit(request, os_id):
    ordem = get_object_or_404(OrdemServico, id=os_id)
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST, instance=ordem)
        if form.is_valid():
            # Se status for ENTREGUE e data_saida vazia, preenche automaticamente
            if form.cleaned_data['status'] == 'ENTREGUE' and not ordem.data_saida:
                ordem.data_saida = timezone.now()
            ordem = form.save(commit=False)
            ordem.save()
            form.save_m2m()
            # Se já havia sido debitado, reverter antes de debitar novamente
            if ordem.estoque_debitado:
                reverter_baixa(ordem)
            debitar_estoque(ordem)
            messages.success(request, 'Ordem de Serviço atualizada com sucesso.')
            return redirect('os_list')
        else:
            messages.error(request, 'Erro ao atualizar OS. Verifique os dados.')
    else:
        form = OrdemServicoForm(instance=ordem)
    context = {'form': form, 'ordem': ordem}
    return render(request, 'inventory/os_form.html', context)


@login_required
def os_detail(request, os_id):
    ordem = get_object_or_404(OrdemServico, id=os_id)
    context = {'ordem': ordem}
    return render(request, 'inventory/os_detail.html', context)


@login_required
def os_finish(request, os_id):
    ordem = get_object_or_404(OrdemServico, id=os_id)
    if request.method == 'POST':
        form = OsFinishForm(request.POST, instance=ordem)
        if form.is_valid():
            entregue = form.cleaned_data.get('entregue')
            if entregue:
                ordem.status = 'ENTREGUE'
                if not ordem.data_saida:
                    ordem.data_saida = timezone.now()
                # Baixa de estoque se ainda não foi efetuada
                debitar_estoque(ordem)
            else:
                # Se não marcar entregue, apenas salva laudo técnico
                pass
            form.save()
            messages.success(request, 'Ordem de Serviço finalizada com sucesso.')
            return redirect('os_list')
        else:
            messages.error(request, 'Erro ao finalizar OS. Verifique os dados.')
    else:
        form = OsFinishForm(instance=ordem)
    context = {'form': form, 'ordem': ordem}
    return render(request, 'inventory/os_finish.html', context)


@login_required
def os_reopen(request, os_id):
    ordem = get_object_or_404(OrdemServico, id=os_id)
    if request.method == 'POST':
        form = OsReopenForm(request.POST)
        if form.is_valid():
            comentario = form.cleaned_data.get('comentario')
            if comentario:
                # Adiciona comentário ao laudo existente
                if ordem.laudo:
                    ordem.laudo += f"\n\n[REABERTURA] {comentario}"
                else:
                    ordem.laudo = f"[REABERTURA] {comentario}"
            ordem.status = 'ABERTO'
            ordem.data_saida = None
            # Reverter baixa de estoque
            reverter_baixa(ordem)
            ordem.save()
            messages.success(request, 'Ordem de Serviço reaberta com sucesso.')
            return redirect('os_list')
        else:
            messages.error(request, 'Erro ao reabrir OS. Verifique os dados.')
    else:
        form = OsReopenForm()
    context = {'form': form, 'ordem': ordem}
    return render(request, 'inventory/os_reopen.html', context)


@login_required
def normalizar_categorias(request):
    categorias = Categoria.objects.all()
    for cat in categorias:
        cat.nome = cat.nome.upper()
        cat.save()
    return HttpResponse("Categorias normalizadas com sucesso.")
