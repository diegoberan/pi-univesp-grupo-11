from django.db import models


class Estado(models.Model):
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=50)

    class Meta:
        ordering = ['sigla']

    def __str__(self):
        return self.sigla


class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='cidades')

    class Meta:
        ordering = ['nome']
        unique_together = ['nome', 'estado']

    def __str__(self):
        return f"{self.nome}/{self.estado.sigla}"


class IES(models.Model):
    STATUS_CHOICES = [
        ('Federal', 'Federal'),
        ('Estadual', 'Estadual'),
        ('Municipal', 'Municipal'),
        ('Privada', 'Privada'),
    ]

    sigla = models.CharField(max_length=30, blank=True)
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=300, blank=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank=True, related_name='ies_list')
    uf = models.CharField(max_length=2)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    homepage = models.URLField(max_length=300, blank=True)
    status_juridico = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    areas_pesquisa = models.TextField(blank=True)
    area_conhecimento = models.CharField(max_length=200, blank=True)
    especializacao = models.BooleanField(default=False)
    nota_especializacao = models.IntegerField(null=True, blank=True)
    mestrado = models.BooleanField(default=False)
    doutorado = models.BooleanField(default=False)
    nota_pos_capes = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'IES'
        verbose_name_plural = 'IES'

    def __str__(self):
        return f"{self.sigla} - {self.nome}" if self.sigla else self.nome


class CursoPos(models.Model):
    GRAU_CHOICES = [
        ('MESTRADO', 'Mestrado'),
        ('DOUTORADO', 'Doutorado'),
        ('MESTRADO PROFISSIONAL', 'Mestrado Profissional'),
    ]

    ies = models.ForeignKey(IES, on_delete=models.CASCADE, related_name='cursos_pos')
    ano_base = models.IntegerField(null=True, blank=True)
    grande_area = models.CharField(max_length=100, blank=True)
    area_conhecimento = models.CharField(max_length=200, blank=True)
    subarea = models.CharField(max_length=200, blank=True)
    especialidade = models.CharField(max_length=200, blank=True)
    area_avaliacao = models.CharField(max_length=200, blank=True)
    nome_programa = models.CharField(max_length=300, blank=True)
    nome_curso = models.CharField(max_length=300, blank=True)
    grau = models.CharField(max_length=30, choices=GRAU_CHOICES, blank=True)
    conceito = models.IntegerField(null=True, blank=True)
    situacao = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['ies__nome', 'nome_curso']

    def __str__(self):
        return f"{self.nome_curso} ({self.grau})"
