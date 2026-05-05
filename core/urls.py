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
from core import views
from inventory import views as inventory_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('tarefa/concluir/<int:tarefa_id>/', views.concluir_tarefa, name='concluir_tarefa'),
    path('tarefa/reabrir/<int:tarefa_id>/', views.reabrir_tarefa, name='reabrir_tarefa'),
    path('tarefa/editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
    path('estoque/', inventory_views.lista_estoque, name='lista_estoque'),
    path('inventory/', include('inventory.urls')),
]
