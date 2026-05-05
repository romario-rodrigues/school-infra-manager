from django.contrib import admin
from core.models import RegistroPonto

@admin.register(RegistroPonto)
class RegistroPontoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data', 'hora_entrada', 'inicio_intervalo', 'fim_intervalo', 'hora_saida', 'horas_extras')
    list_filter = ('usuario', 'data')
    search_fields = ('usuario__username',)
