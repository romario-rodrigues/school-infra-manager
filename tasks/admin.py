from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Tarefa

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'prioridade', 'status', 'previsao_conclusao')
    list_filter = ('status', 'prioridade')
    search_fields = ('titulo', 'descricao')
    list_editable = ('status', 'prioridade') # Permite mudar o status direto na lista!