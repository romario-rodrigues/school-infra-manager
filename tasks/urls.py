from django.urls import path
from . import views

urlpatterns = [
    # Caminho: /tasks/atualizar-status/ID/STATUS/
    path('atualizar-status/<int:tarefa_id>/<str:novo_status>/', views.atualizar_status, name='atualizar_status'),
]