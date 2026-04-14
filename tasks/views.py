from django.shortcuts import get_object_or_404, redirect # Import correto aqui
from .models import Tarefa
from django.contrib.auth.decorators import login_required

@login_required
def atualizar_status(request, tarefa_id, novo_status):
    # Busca a tarefa ou retorna erro 404 se não existir
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    
    # Atualiza o status com o que veio da URL
    tarefa.status = novo_status
    tarefa.save()
    
    # Redireciona de volta para a dashboard
    return redirect('dashboard')