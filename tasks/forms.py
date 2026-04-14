from django import forms
from .models import Tarefa

class TarefaRapidaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'prioridade']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nova tarefa...'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
        }