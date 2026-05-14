from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Categorias"
        ordering = ['nome']

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
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.quantidade_atual})"

    @property
    def precisa_repor(self):
        # Usando o nome correto que definimos acima
        return self.quantidade_atual <= self.quantidade_minima

    @property
    def subtotal(self):
        return self.quantidade_atual * self.preco_unitario

    @classmethod
    def total_geral(cls):
        from django.db.models import Sum, F
        result = cls.objects.aggregate(total=Sum(F('quantidade_atual') * F('preco_unitario')))
        return result['total'] or 0


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


class OrdemServico(models.Model):
    SETORES = (
        ('ADM', 'Administrativo'),
        ('PED', 'Pedagógico'),
        ('INF', 'Informática'),
        ('OUT', 'Outro'),
    )

    STATUS_CHOICES = (
        ('ABERTO', 'Aberto'),
        ('EM_MANUTENCAO', 'Em Manutenção'),
        ('AGUARDANDO_PECA', 'Aguardando Peça'),
        ('CONCLUIDO', 'Concluído'),
        ('ENTREGUE', 'Entregue'),
    )

    setor = models.CharField(max_length=3, choices=SETORES, default='OUT')
    solicitante = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    numero_serie = models.CharField(max_length=200)
    defeito = models.TextField()
    laudo = models.TextField(blank=True, null=True)
    laudo_tecnico = models.TextField(blank=True, null=True, verbose_name='Laudo Técnico')
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    itens = models.ManyToManyField(ItemEstoque, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField(null=True, blank=True, verbose_name='Data de Saída')

    def save(self, *args, **kwargs):
        self.solicitante = self.solicitante.upper()
        self.marca = self.marca.upper()
        self.modelo = self.modelo.upper()
        self.numero_serie = self.numero_serie.upper()
        self.defeito = self.defeito.upper()
        if self.laudo:
            self.laudo = self.laudo.upper()
        if self.laudo_tecnico:
            self.laudo_tecnico = self.laudo_tecnico.upper()
        # Preenche data_saida automaticamente quando status for ENTREGUE
        if self.status == 'ENTREGUE' and not self.data_saida:
            from django.utils import timezone
            self.data_saida = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OS {self.id} - {self.solicitante} ({self.get_setor_display()})"

    class Meta:
        verbose_name_plural = "Ordens de Serviço"
        ordering = ['-data_criacao']
