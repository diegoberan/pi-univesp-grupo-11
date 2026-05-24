# PI-UNIVESP Grupo 11 — Plataforma Georreferenciada de Pós-Graduação

Mapa interativo para buscar programas de pós-graduação no Brasil, com dados da CAPES e MEC.

## Stack

- Django 5 + SQLite
- Leaflet.js + OpenStreetMap (mapa)
- Bootstrap 5.3 (UI)
- Chart.js 4.4 (dashboard)

## Pré-requisitos

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recomendado) ou pip

## Como rodar

### Com uv (recomendado)

```bash
# 1. Criar venv e instalar dependências
uv venv .venv --python 3.10
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

uv pip install -r requirements.txt

# 2. Aplicar migrations
python manage.py migrate

# 3. Popular banco de dados (só na primeira vez)
python manage.py importar_dados data/ies.csv data/cursos.csv

# 4. Rodar servidor
python manage.py runserver
```

### Com pip

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py importar_dados data/ies.csv data/cursos.csv
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## URLs

| URL | Descrição |
|-----|-----------|
| `/` | Mapa interativo com clusters |
| `/consulta/` | Tabela com filtros e exportar CSV |
| `/dashboard/` | Estatísticas e gráficos |
| `/ies/<id>/` | Detalhes de uma IES |

## Dados

Fonte: CAPES (Coordenação de Aperfeiçoamento de Pessoal de Nível Superior) + MEC.
Arquivos na branch `Base-de-Dados` do repositório.

- `data/ies.csv` — 576 IES com coordenadas geográficas
- `data/cursos.csv` — 7488 cursos de pós-graduação (mestrado, doutorado, especialização)
