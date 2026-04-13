from django.db import models

# Create your models here.

from django.db import models

class Equipamento(models.Model):
    TIPOS = (
        ('SW', 'Switch'),
        ('AP', 'Access Point'),
        ('SRV', 'Servidor'),
        ('OUT', 'Outro'),
    )

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=3, choices=TIPOS)
    marca = models.CharField(max_length=50, blank=True) # Ex: MikroTik, Ubiquiti
    modelo = models.CharField(max_length=50, blank=True)
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, blank=True, null=True)
    mac = models.CharField(max_length=17, blank=True)
    localizacao = models.CharField(max_length=200, help_text="Ex: Sala 05, Bloco B")
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} - {self.ip}"

class Camera(models.Model):
    nome = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(blank=True, null=True)
    nvr_channel = models.IntegerField(verbose_name="Canal no NVR", blank=True, null=True)
    tecnologia = models.CharField(max_length=50, choices=(('IP', 'IP'), ('AN', 'Analógica')), default='IP')
    localizacao = models.CharField(max_length=200)
    status_ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
