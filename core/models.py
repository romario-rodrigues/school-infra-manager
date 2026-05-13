from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class RegistroPonto(models.Model):
    # Relaciona o ponto ao usuário que você criou
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    
    # Registros de horários
    entrada = models.DateTimeField(null=True, blank=True)
    inicio_intervalo = models.DateTimeField(null=True, blank=True)
    fim_intervalo = models.DateTimeField(null=True, blank=True)
    saida = models.DateTimeField(null=True, blank=True)
    
    # Campo para armazenar o cálculo das horas extras
    horas_extras = models.DurationField(null=True, blank=True, default=timedelta(0))

    class Meta:
        verbose_name = "Registro de Ponto"
        verbose_name_plural = "Registros de Ponto"

    def __str__(self):
        return f"{self.usuario.username} - {self.data}"