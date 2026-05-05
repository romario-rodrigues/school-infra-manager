from django.contrib import admin
from .models import SaidaEstoque

@admin.register(SaidaEstoque)
class SaidaEstoqueAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantidade', 'data_hora', 'local', 'tipo_equipamento')
    list_filter = ('tipo_equipamento', 'data_hora')
    search_fields = ('item__nome', 'local')
