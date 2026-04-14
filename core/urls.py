"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core.views import dashboard, concluir_tarefa, reabrir_tarefa # Importe as funções aqui

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('tarefa/concluir/<int:tarefa_id>/', concluir_tarefa, name='concluir_tarefa'),
    path('tarefa/reabrir/<int:tarefa_id>/', reabrir_tarefa, name='reabrir_tarefa'),
    # Mantenha as outras rotas de estoque/infra que você já tinha abaixo
]
