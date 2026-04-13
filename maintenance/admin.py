
from django.contrib import admin
from .models import RegistroManutencao

@admin.register(RegistroManutencao)
class RegistroManutencaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'get_alvo', 'tipo', 'tecnico')
    list_filter = ('tipo', 'data')
    search_fields = ('descricao', 'tecnico')

    def get_alvo(self, obj):
        return obj.camera if obj.camera else obj.equipamento
    get_alvo.short_description = 'Equipamento/Câmera'