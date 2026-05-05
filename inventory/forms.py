from django import forms
from .models import ItemEstoque, Categoria, SaidaEstoque

class ItemEstoqueForm(forms.ModelForm):
    class Meta:
        model = ItemEstoque
        fields = ['nome', 'categoria', 'quantidade_atual', 'quantidade_minima', 'unidade_medida', 'localizacao_fisica']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Item'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_atual': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qtd'}),
            'quantidade_minima': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mín'}),
            'unidade_medida': forms.Select(attrs={'class': 'form-select'}),
            'localizacao_fisica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local'}),
        }

class SaidaEstoqueForm(forms.ModelForm):
    class Meta:
        model = SaidaEstoque
        fields = ['item', 'quantidade', 'local', 'tipo_equipamento']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local da saída'}),
            'tipo_equipamento': forms.Select(attrs={'class': 'form-select'}),
        }
