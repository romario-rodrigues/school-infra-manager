from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from infrastructure.models import Camera, Equipamento
from inventory.models import ItemEstoque
from infrastructure.utils import ping_host # Importe a função

@login_required
def dashboard(request):
    cameras = Camera.objects.all()
    # Criamos uma lista de dicionários com o status real (ping)
    status_cameras = []
    cameras_online = 0
    
    for cam in cameras:
        online = ping_host(cam.ip)
        if online:
            cameras_online += 1
        status_cameras.append({
            'nome': cam.nome,
            'ip': cam.ip,
            'online': online
        })

    total_cameras = cameras.count()
    cameras_off = total_cameras - cameras_online
    itens_baixo_estoque = [item for item in ItemEstoque.objects.all() if item.precisa_repor]

    context = {
        'total_cameras': total_cameras,
        'cameras_online': cameras_online,
        'cameras_off': cameras_off,
        'status_cameras': status_cameras, # Lista com status real
        'itens_baixo_estoque': itens_baixo_estoque,
    }
    return render(request, 'dashboard.html', context)