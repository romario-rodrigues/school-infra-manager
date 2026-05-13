from django.contrib import admin
from .models import RegistroPonto

@admin.register(RegistroPonto)
class RegistroPontoAdmin(admin.ModelAdmin):
    # Ajustando os nomes para baterem com o models.py
    list_display = ('usuario', 'data', 'entrada', 'inicio_intervalo', 'fim_intervalo', 'saida', 'horas_extras')
    list_filter = ('data', 'usuario')
    search_fields = ('usuario__username', 'data')
