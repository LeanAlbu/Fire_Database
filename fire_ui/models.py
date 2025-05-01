# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FocosDeQueimada(models.Model):
    id_queimada = models.AutoField(primary_key=True)
    data_hora = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=3)
    longitude = models.DecimalField(max_digits=9, decimal_places=3)
    potencia_rad = models.FloatField()
    id_municipio = models.ForeignKey('Municipios', models.DO_NOTHING, db_column='id_municipio', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'focos_de_queimada'
        unique_together = (('data_hora', 'latitude', 'longitude'),)


class Municipios(models.Model):
    id_municipio = models.IntegerField(primary_key=True)
    nome_municipio = models.CharField(unique=True, max_length=50)
    area_km2 = models.DecimalField(max_digits=6, decimal_places=2)
    populacao = models.IntegerField()
    codigo_regiao = models.ForeignKey('RegioesImediatas', models.DO_NOTHING, db_column='codigo_regiao')

    class Meta:
        managed = False
        db_table = 'municipios'


class RegioesImediatas(models.Model):
    codigo_regiao = models.IntegerField(primary_key=True)
    bioma = models.CharField(max_length=30)
    area_km2 = models.DecimalField(max_digits=10, decimal_places=2)
    nome_regiao = models.CharField(unique=True, max_length=50)
    clima_regiao = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'regioes_imediatas'

class SateliteQueimada(models.Model):
    id = models.AutoField(primary_key=True)  # Chave primária real usada pelo Django/Admin
    id_queimada = models.ForeignKey(FocosDeQueimada, models.DO_NOTHING, db_column='id_queimada')
    id_satelite = models.ForeignKey('Satelites', models.DO_NOTHING, db_column='id_satelite')

    class Meta:
        db_table = 'satelite_queimada'
        unique_together = (('id_queimada', 'id_satelite'),)

class Satelites(models.Model):
    id_satelite = models.AutoField(primary_key=True)
    nome_satelite = models.CharField(unique=True, max_length=30)
    agencia = models.CharField(max_length=50)
    tipo_orbita = models.CharField(max_length=50)
    status_operacional = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'satelites'
