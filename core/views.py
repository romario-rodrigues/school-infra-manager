from django.shortcuts import render, redirect # Unificamos os dois imports aqui
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef 
from infrastructure.models import Camera, Equipamento
from inventory.models import ItemEstoque
from maintenance.models import RegistroManutencao 
from infrastructure.utils import ping_host
from tasks.models import Tarefa
from tasks.forms import TarefaRapidaForm # Adicionamos o nome do formulário

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

    # 3. Busca de Dados para os Cards e Listas
    total_cameras = cameras.count()
    cameras_off = total_cameras - cameras_online
    itens_baixo_estoque = [item for item in ItemEstoque.objects.all() if item.precisa_repor]
    
    # ESSA LINHA PRECISA ESTAR AQUI FORA PARA SEMPRE SER EXECUTADA:
    tarefas_pendentes = Tarefa.objects.exclude(status='Concluido').order_by('prioridade')

    context = {
        'total_cameras': total_cameras,
        'cameras_online': cameras_online,
        'cameras_off': cameras_off,
        'status_cameras': status_cameras,
        'itens_baixo_estoque': itens_baixo_estoque,
        'form': form,
        'tarefas_pendentes': tarefas_pendentes,
    }
    return render(request, 'dashboard.html', context)