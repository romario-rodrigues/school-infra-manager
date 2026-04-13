from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Categorias"

class ItemEstoque(models.Model):
    UNIDADES = (
        ('Unidade', 'Unidade'),
        ('Metros', 'Metros'),
        ('Pacote', 'Pacote'),
    )

    nome = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    quantidade_atual = models.IntegerField(default=0)
    quantidade_minima = models.IntegerField(default=5)
    unidade_medida = models.CharField(max_length=20, default="Unidade", choices=UNIDADES)
    localizacao_fisica = models.CharField(max_length=100)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.quantidade_atual})"

    @property
    def precisa_repor(self):
        return self.quantidade_atual <= self.quantidade_minima