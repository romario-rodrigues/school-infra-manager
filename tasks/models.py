from django.db import models
from django.utils import timezone

class Tarefa(models.Model):
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Execução', 'Em Execução'),
        ('Aguardando', 'Aguardando Terceiro'),
        ('Concluido', 'Concluído'),
    )
    
    PRIORIDADE_CHOICES = (
        ('Baixa', 'Baixa'),
        ('Media', 'Média'),
        ('Alta', 'Alta'),
        ('Critica', 'Crítica (Urgente)'),
    )

    titulo = models.CharField(max_length=200)
    descricao_detalhada = models.TextField(blank=True, null=True, verbose_name="Relato Técnico")
    prioridade = models.CharField(max_length=20, choices=[('Baixa', 'Baixa'), ('Alta', 'Alta'), ('Critica', 'Critica')])
    status = models.CharField(max_length=20, default='Pendente')
    criado_em = models.DateTimeField(auto_now_add=True)
    previsao_conclusao = models.DateField(null=True, blank=True)

    # Novos campos de data
    data_criacao = models.DateTimeField(auto_now_add=True) # Grava sozinho ao criar
    data_conclusao = models.DateTimeField(null=True, blank=True) # Preencheremos quando concluir

    """def __str__(self):
        return f"{self.titulo} - {self.status}"""
    
    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"