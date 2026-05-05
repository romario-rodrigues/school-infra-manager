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
    # Mude a linha da categoria para permitir vazio (null e blank)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    quantidade_atual = models.IntegerField(default=0)
    quantidade_minima = models.IntegerField(default=5)
    unidade_medida = models.CharField(max_length=20, default="Unidade", choices=UNIDADES)
    localizacao_fisica = models.CharField(max_length=100, blank=True, null=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.quantidade_atual})"

    @property
    def precisa_repor(self):
        # Usando o nome correto que definimos acima
        return self.quantidade_atual <= self.quantidade_minima


class SaidaEstoque(models.Model):
    TIPOS_EQUIPAMENTO = (
        ('SW', 'Switch'),
        ('AP', 'Access Point'),
        ('SRV', 'Servidor'),
        ('OUT', 'Outro'),
    )

    item = models.ForeignKey(ItemEstoque, on_delete=models.CASCADE, related_name='saidas')
    quantidade = models.PositiveIntegerField()
    data_hora = models.DateTimeField(auto_now_add=True)
    local = models.CharField(max_length=200)
    tipo_equipamento = models.CharField(max_length=3, choices=TIPOS_EQUIPAMENTO, default='OUT')

    def __str__(self):
        return f"{self.item.nome} - {self.quantidade} ({self.get_tipo_equipamento_display()})"

    class Meta:
        verbose_name_plural = "Saídas de Estoque"
