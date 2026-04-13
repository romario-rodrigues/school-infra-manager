from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef # Adicione o OuterRef aqui
from infrastructure.models import Camera, Equipamento
from inventory.models import ItemEstoque
from maintenance.models import RegistroManutencao # Importe o modelo novo
from infrastructure.utils import ping_host

@login_required
def dashboard(request):
    # Verifica se existe manutenção para cada câmera
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
            'tem_manutencao': cam.tem_manutencao # Passamos a informação para o template
        })

    total_cameras = cameras.count()
    cameras_off = total_cameras - cameras_online
    itens_baixo_estoque = [item for item in ItemEstoque.objects.all() if item.precisa_repor]

    context = {
        'total_cameras': total_cameras,
        'cameras_online': cameras_online,
        'cameras_off': cameras_off,
        'status_cameras': status_cameras,
        'itens_baixo_estoque': itens_baixo_estoque,
    }
    return render(request, 'dashboard.html', context)