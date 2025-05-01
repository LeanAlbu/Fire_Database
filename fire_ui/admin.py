from django.contrib import admin
from .models import FocosDeQueimada, Municipios, RegioesImediatas, SateliteQueimada, Satelites

@admin.register(FocosDeQueimada)
class FocosDeQueimadaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FocosDeQueimada._meta.fields]
    search_fields = ['id']  # Ajuste conforme os campos da sua tabela

@admin.register(Municipios)
class MunicipiosAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Municipios._meta.fields]
    search_fields = ['nome']  # Ajuste conforme os campos da sua tabela

@admin.register(RegioesImediatas)
class RegioesImediatasAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RegioesImediatas._meta.fields]
    search_fields = ['nome']  # Ajuste conforme os campos da sua tabela

@admin.register(SateliteQueimada)
class SateliteQueimadaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SateliteQueimada._meta.fields]
    search_fields = ['id']  # Ajuste conforme os campos da sua tabela

@admin.register(Satelites)
class SatelitesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Satelites._meta.fields]
    search_fields = ['nome']  # Ajuste conforme os campos da sua tabela
