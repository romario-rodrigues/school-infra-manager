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
from .views import dashboard # Importe a view que criamos
from .views import concluir_tarefa # Importe a nova função
from .views import reabrir_tarefa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'), # Rota para a página inicial
<<<<<<< HEAD
    path('tarefa/concluir/<int:tarefa_id>/', concluir_tarefa, name='concluir_tarefa'),
    path('tarefa/reabrir/<int:tarefa_id>/', reabrir_tarefa, name='reabrir_tarefa'),
=======
    path('tasks/', include('tasks.urls')),
>>>>>>> dd48179a5d0698d7f6e5890e283267de76eda8b2
]
