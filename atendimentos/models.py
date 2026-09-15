from django.core.exceptions import ValidationError
from django.db import models


class Profissional(models.Model):
    nome = models.CharField(max_length=150)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    nome_completo = models.CharField(max_length=200)
    data_nascimento = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo


class Grupo(models.Model):
    nome = models.CharField(max_length=120)
    dia_semana = models.PositiveSmallIntegerField(choices=[(0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'), (3, 'Quinta'), (4, 'Sexta'), (5, 'Sábado'), (6, 'Domingo')])
    horario = models.TimeField()
    profissional_1 = models.ForeignKey(Profissional, on_delete=models.PROTECT, related_name='grupos_1')
    profissional_2 = models.ForeignKey(Profissional, on_delete=models.PROTECT, related_name='grupos_2')
    usuarios = models.ManyToManyField(Usuario, through='Participacao', related_name='grupos')
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['dia_semana', 'horario', 'nome']

    def clean(self):
        if self.profissional_1_id and self.profissional_1_id == self.profissional_2_id:
            raise ValidationError('Selecione dois profissionais diferentes.')

    def __str__(self):
        return f'{self.nome} — {self.get_dia_semana_display()} {self.horario:%H:%M}'


class Participacao(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    ativo = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['grupo', 'usuario'], name='participacao_unica')]

    def clean(self):
        if self.ativo and self.grupo_id:
            quantidade = Participacao.objects.filter(grupo_id=self.grupo_id, ativo=True).exclude(pk=self.pk).count()
            if quantidade >= 10:
                raise ValidationError('Cada grupo pode ter no máximo 10 usuários ativos.')

    def __str__(self):
        return f'{self.usuario} em {self.grupo}'


class Registro(models.Model):
    PRESENCA = 'P'
    FALTA = 'F'
    FJ = 'FJ'
    FAMILIAR = 'AF'
    EXTRA = 'AE'
    TIPOS = [(PRESENCA, 'Presença'), (FALTA, 'Falta'), (FJ, 'FJ'), (FAMILIAR, 'Atendimento Familiar'), (EXTRA, 'Atendimento Extra')]
    data = models.DateField()
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=2, choices=TIPOS)
    observacao = models.CharField(max_length=250, blank=True)
    registrado_em = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['data', 'grupo', 'usuario'], name='registro_diario_unico')]
        ordering = ['data', 'grupo__horario', 'usuario__nome_completo']

    def __str__(self):
        return f'{self.data} — {self.usuario}: {self.get_tipo_display()}'


class Configuracao(models.Model):
    email_destino = models.EmailField(blank=True)

    def __str__(self):
        return 'Configuração de envio'
