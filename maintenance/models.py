from django.db import models

# Create your models here.
from django.db import models
from infrastructure.models import Camera, Equipamento

class RegistroManutencao(models.Model):
    TIPOS = (
        ('Preventiva', 'Preventiva'),
        ('Corretiva', 'Corretiva'),
        ('Instalação', 'Instalação'),
    )

    data = models.DateTimeField(auto_now_add=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, null=True, blank=True)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='Corretiva')
    descricao = models.TextField(verbose_name="O que foi feito?")
    tecnico = models.CharField(max_length=100, default="Romário Rodrigues")
    custo_material = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        alvo = self.camera.nome if self.camera else self.equipamento.nome
        return f"{self.data.strftime('%d/%m/%Y')} - {alvo}"

    class Meta:
        verbose_name = "Registro de Manutenção"
        verbose_name_plural = "Registros de Manutenção"