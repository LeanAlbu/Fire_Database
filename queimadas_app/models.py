from django.db import models

class RegiaoImediata(models.Model):
    bioma = models.CharField(max_length=30)
    nome_regiao = models.CharField(max_length=50, unique=True)
    clima_regiao = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Região Imediata"
        verbose_name_plural = "Regiões Imediatas"

    def __str__(self):
        return self.nome_regiao


class Municipio(models.Model):
    nome_municipio = models.CharField(max_length=50, unique=True)
    area_km2 = models.DecimalField(max_digits=6, decimal_places=2)
    populacao = models.IntegerField()
    id_regiao = models.ForeignKey(RegiaoImediata, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"
        constraints = [
            models.CheckConstraint(check=models.Q(area_km2__gt=0), name='ck_area_positiva')
        ]

    def __str__(self):
        return self.nome_municipio


ORBITA_CHOICES = [
    ('LEO', 'Órbita Terrestre Baixa'),
    ('GEO', 'Órbita Geossíncrona'),
    ('MEO', 'Órbita Terrestre Média'),
]

class Satelite(models.Model):
    nome_satelite = models.CharField(max_length=100)
    pais_origem = models.CharField(max_length=50)
    tipo_orbita = models.CharField(max_length=50, choices=ORBITA_CHOICES)

    def __str__(self):
        return self.nome_satelite


class FocoQueimada(models.Model):
    data_hora = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=3)
    longitude = models.DecimalField(max_digits=9, decimal_places=3)
    potencia_rad = models.FloatField()
    id_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
    satelites = models.ManyToManyField(Satelite, through='SateliteQueimada')

    class Meta:
        verbose_name = "Foco de Queimada"
        verbose_name_plural = "Focos de Queimada"
        constraints = [
            models.UniqueConstraint(fields=['data_hora', 'latitude', 'longitude'], name='unq_foco_queimada'),
        ]

    def __str__(self):
        return f"Foco em {self.data_hora}"


class SateliteQueimada(models.Model):
    id_queimada = models.ForeignKey(FocoQueimada, on_delete=models.CASCADE)
    id_satelite = models.ForeignKey(Satelite, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Relação Satélite-Queimada"
        verbose_name_plural = "Relações Satélite-Queimada"
        constraints = [
            models.UniqueConstraint(fields=['id_queimada', 'id_satelite'], name='pk_ligacao_queimada_satelite')
        ]

    def __str__(self):
        return f"{self.id_satelite} - {self.id_queimada}"
