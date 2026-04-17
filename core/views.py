from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef 
from django.utils import timezone

# Imports dos seus modelos
from infrastructure.models import Camera, Equipamento
from inventory.models import ItemEstoque
from maintenance.models import RegistroManutencao 
from infrastructure.utils import ping_host
from tasks.models import Tarefa
from tasks.forms import TarefaRapidaForm

@login_required
def concluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.status = 'Concluido'
    tarefa.data_conclusao = timezone.now()
    tarefa.save()
    return redirect('dashboard')

@login_required
def reabrir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.status = 'Pendente'
    tarefa.data_conclusao = None
    tarefa.save()
    return redirect('dashboard')

@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    if request.method == 'POST':
        tarefa.titulo = request.POST.get('titulo')
        tarefa.prioridade = request.POST.get('prioridade')
        # ESTA LINHA ABAIXO É A CHAVE:
        tarefa.descricao_detalhada = request.POST.get('descricao_detalhada') 
        tarefa.save()
        return redirect('dashboard')
    return render(request, 'editar_tarefa.html', {'tarefa': tarefa})

@login_required
def dashboard(request):
    # 1. Lógica do Formulário (POST)
    if request.method == 'POST':
        form = TarefaRapidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TarefaRapidaForm()

    # 2. Lógica das Câmeras (Ping)
    manutencoes = RegistroManutencao.objects.filter(camera=OuterRef('pk'))
    cameras = Camera.objects.annotate(tem_manutencao=Exists(manutencoes))
    
    status_cameras = []
    cameras_online = 0
    
    for cam in cameras:
        online = ping_host(cam.ip)
        if online:
            cameras_online += 1
        status_cameras.append({
            'nome': cam.nome,
            'ip': cam.ip,
            'online': online,
            'tem_manutencao': cam.tem_manutencao 
        })

    # 3. Dados para Cards e Listas
    total_cameras = cameras.count()
    cameras_off = total_cameras - cameras_online
    itens_baixo_estoque = [item for item in ItemEstoque.objects.all() if item.precisa_repor]
    
    # Listas de Tarefas
    tarefas_pendentes = Tarefa.objects.exclude(status='Concluido').order_by('-data_criacao')
    historico_tarefas = Tarefa.objects.filter(status='Concluido').order_by('-data_conclusao')[:10]

    context = {
        'total_cameras': total_cameras,
        'cameras_online': cameras_online,
        'cameras_off': cameras_off,
        'status_cameras': status_cameras,
        'itens_baixo_estoque': itens_baixo_estoque,
        'form': form,
        'tarefas_pendentes': tarefas_pendentes,
        'historico_tarefas': historico_tarefas,
    }
    return render(request, 'dashboard.html', context)