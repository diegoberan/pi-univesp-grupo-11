from django.contrib import admin
from .models import Estado, Cidade, IES, CursoPos


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nome']
    search_fields = ['sigla', 'nome']


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'estado']
    list_filter = ['estado']
    search_fields = ['nome']


@admin.register(IES)
class IESAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nome', 'uf', 'status_juridico', 'mestrado', 'doutorado']
    list_filter = ['uf', 'status_juridico', 'mestrado', 'doutorado', 'especializacao']
    search_fields = ['nome', 'sigla']
    list_per_page = 50


@admin.register(CursoPos)
class CursoPosAdmin(admin.ModelAdmin):
    list_display = ['nome_curso', 'ies', 'grau', 'conceito', 'situacao']
    list_filter = ['grau', 'conceito', 'situacao', 'grande_area']
    search_fields = ['nome_curso', 'nome_programa', 'ies__nome']
    list_per_page = 50
