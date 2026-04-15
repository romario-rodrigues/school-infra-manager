from django.shortcuts import render, redirect, get_object_or_404
from tasks.models import Tarefa # Importante para achar o modelo
from django.contrib.auth.decorators import login_required

@login_required
def atualizar_status(request, tarefa_id, novo_status):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.status = novo_status
    tarefa.save()
    return redirect('dashboard')

@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)

    if request.method == 'POST':
        novo_titulo = request.POST.get('titulo')
        nova_prioridade = request.POST.get('prioridade')

        if novo_titulo:
            tarefa.titulo = novo_titulo
            tarefa.prioridade = nova_prioridade
            tarefa.save()
            return redirect('dashboard') # Redireciona APÓS salvar

    # Se não for POST (ou seja, se estiver apenas abrindo a página), renderiza o HTML
    return render(request, 'editar_tarefa.html', {'tarefa': tarefa})