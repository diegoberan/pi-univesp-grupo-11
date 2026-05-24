import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from ies.models import Estado, Cidade, IES, CursoPos


class Command(BaseCommand):
    help = 'Importa dados dos CSVs para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ies',
            default='data/ies.csv',
            help='Caminho para o CSV de IES georreferenciadas'
        )
        parser.add_argument(
            '--cursos',
            default='data/cursos.csv',
            help='Caminho para o CSV de cursos de pos-graduacao'
        )

    def handle(self, *args, **options):
        ies_path = options['ies']
        cursos_path = options['cursos']

        if not os.path.exists(ies_path):
            self.stderr.write(self.style.ERROR(f'Arquivo nao encontrado: {ies_path}'))
            return
        if not os.path.exists(cursos_path):
            self.stderr.write(self.style.ERROR(f'Arquivo nao encontrado: {cursos_path}'))
            return

        self.importar_ies(ies_path)
        self.importar_cursos(cursos_path)

    def limpar_float(self, valor):
        """Converte lat/long do formato BR (virgula) para float"""
        if not valor or valor.strip() == '':
            return None
        try:
            return float(valor.replace(',', '.'))
        except (ValueError, AttributeError):
            return None

    def limpar_int(self, valor):
        if not valor or valor.strip() == '':
            return None
        try:
            return int(valor)
        except (ValueError, AttributeError):
            return None

    @transaction.atomic
    def importar_ies(self, path):
        self.stdout.write(self.style.WARNING(f'Importando IES de {path}...'))

        # Cache de estados e cidades
        estados_cache = {}
        cidades_cache = {}

        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                uf = row.get('UF', '').strip()
                municipio = row.get('Município', '').strip()

                # Estado
                if uf and uf not in estados_cache:
                    estado, _ = Estado.objects.get_or_create(
                        sigla=uf,
                        defaults={'nome': uf}
                    )
                    estados_cache[uf] = estado

                # Cidade
                cidade = None
                if uf and municipio:
                    cidade_key = f"{uf}:{municipio}"
                    if cidade_key not in cidades_cache:
                        cidade, _ = Cidade.objects.get_or_create(
                            nome=municipio,
                            estado=estados_cache[uf]
                        )
                        cidades_cache[cidade_key] = cidade
                    else:
                        cidade = cidades_cache[cidade_key]

                # IES
                nome = row.get('IES - NOME', '').strip()
                if not nome:
                    continue

                ies, created = IES.objects.update_or_create(
                    nome=nome,
                    defaults={
                        'sigla': row.get('IES - SIGLA', '').strip(),
                        'endereco': row.get('Endereço', '').strip(),
                        'cidade': cidade,
                        'uf': uf,
                        'latitude': self.limpar_float(row.get('Latitude')),
                        'longitude': self.limpar_float(row.get('Longitude')),
                        'homepage': row.get('Homepage', '').strip(),
                        'status_juridico': row.get('Status Jurídico', '').strip(),
                        'areas_pesquisa': row.get('Áreas de pesquisa', '').strip(),
                        'area_conhecimento': row.get('Área Conhecimento', '').strip(),
                        'especializacao': row.get('Especialização', '').strip().upper() == 'SIM',
                        'nota_especializacao': self.limpar_int(row.get('Nota de Avaliação – Especialização – MEC')),
                        'mestrado': row.get('Mestrado', '').strip().upper() == 'SIM',
                        'doutorado': row.get('Doutorado', '').strip().upper() == 'SIM',
                        'nota_pos_capes': self.limpar_int(row.get('Nota de Avaliação – Pós-graduação – Capes')),
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'  {count} IES importadas'))

    @transaction.atomic
    def importar_cursos(self, path):
        self.stdout.write(self.style.WARNING(f'Importando cursos de pos de {path}...'))

        # Cache de IES por sigla
        ies_cache = {}
        for ies in IES.objects.all():
            if ies.sigla:
                ies_cache[ies.sigla.strip()] = ies

        count = 0
        skipped = 0

        with open(path, encoding='latin-1') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                sigla = row.get('SG_ENTIDADE_ENSINO', '').strip()
                if not sigla:
                    skipped += 1
                    continue

                # Busca IES pela sigla
                ies = ies_cache.get(sigla)
                if not ies:
                    # Tenta buscar no banco
                    try:
                        ies = IES.objects.get(sigla__iexact=sigla)
                        ies_cache[sigla] = ies
                    except IES.DoesNotExist:
                        # Cria IES basica se nao existe
                        ies = IES.objects.create(
                            sigla=sigla,
                            nome=row.get('NM_ENTIDADE_ENSINO', '').strip(),
                            uf=row.get('SG_UF_PROGRAMA', '').strip(),
                        )
                        ies_cache[sigla] = ies

                CursoPos.objects.create(
                    ies=ies,
                    ano_base=self.limpar_int(row.get('AN_BASE')),
                    grande_area=row.get('NM_GRANDE_AREA_CONHECIMENTO', '').strip(),
                    area_conhecimento=row.get('NM_AREA_CONHECIMENTO', '').strip(),
                    subarea=row.get('NM_SUBAREA_CONHECIMENTO', '').strip(),
                    especialidade=row.get('NM_ESPECIALIDADE', '').strip(),
                    area_avaliacao=row.get('NM_AREA_AVALIACAO', '').strip(),
                    nome_programa=row.get('NM_PROGRAMA_IES', '').strip(),
                    nome_curso=row.get('NM_CURSO', '').strip(),
                    grau=row.get('NM_GRAU_CURSO', '').strip(),
                    conceito=self.limpar_int(row.get('CD_CONCEITO_CURSO')),
                    situacao=row.get('DS_SITUACAO_CURSO', '').strip(),
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'  {count} cursos importados ({skipped} ignorados)'))
