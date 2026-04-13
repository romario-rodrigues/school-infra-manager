from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Equipamento, Camera

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'ip', 'localizacao')
    search_fields = ('nome', 'ip', 'mac')

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ip', 'nvr_channel', 'status_ativo')
