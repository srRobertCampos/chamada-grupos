from django.contrib import admin
from .models import Profissional, Usuario, Grupo, Participacao, Registro, Configuracao


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    search_fields = ('nome',)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'data_nascimento', 'ativo')
    search_fields = ('nome_completo',)
    list_filter = ('ativo',)


class ParticipacaoInline(admin.TabularInline):
    model = Participacao
    extra = 1
    autocomplete_fields = ('usuario',)


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dia_semana', 'horario', 'profissional_1', 'profissional_2', 'ativo')
    list_filter = ('dia_semana', 'ativo')
    inlines = (ParticipacaoInline,)


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('data', 'grupo', 'usuario', 'tipo')
    list_filter = ('data', 'tipo', 'grupo')
    search_fields = ('usuario__nome_completo',)


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('email_destino',)
