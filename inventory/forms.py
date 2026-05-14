from django import forms
from .models import ItemEstoque, Categoria, SaidaEstoque, OrdemServico

class ItemEstoqueForm(forms.ModelForm):
    class Meta:
        model = ItemEstoque
        fields = ['nome', 'categoria', 'quantidade_atual', 'quantidade_minima', 'unidade_medida', 'localizacao_fisica', 'preco_unitario']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Item'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_atual': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qtd'}),
            'quantidade_minima': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mín'}),
            'unidade_medida': forms.Select(attrs={'class': 'form-select'}),
            'localizacao_fisica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço Unitário', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all().order_by('nome')

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


class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['setor', 'solicitante', 'marca', 'modelo', 'numero_serie', 'defeito', 'laudo', 'valor', 'itens']
        widgets = {
            'setor': forms.Select(attrs={'class': 'form-select'}),
            'solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solicitante'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nº Série'}),
            'defeito': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Defeito'}),
            'laudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Laudo'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor', 'step': '0.01'}),
            'itens': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
