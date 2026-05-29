import csv
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q
from .models import IES, CursoPos, Estado, Cidade


def index(request):
    """Pagina principal com mapa interativo"""
    estados = Estado.objects.all()
    status_list = IES.objects.values_list('status_juridico', flat=True).distinct().order_by('status_juridico')
    context = {
        'estados': estados,
        'status_list': [s for s in status_list if s],
    }
    return render(request, 'ies/index.html', context)


def api_ies(request):
    """API JSON para o mapa - retorna IES filtradas"""
    qs = IES.objects.filter(latitude__isnull=False, longitude__isnull=False)

    # Filtros
    uf = request.GET.get('uf')
    if uf:
        qs = qs.filter(uf=uf)

    status = request.GET.get('status')
    if status:
        qs = qs.filter(status_juridico=status)

    modalidade = request.GET.get('modalidade')
    if modalidade == 'mestrado':
        qs = qs.filter(mestrado=True)
    elif modalidade == 'doutorado':
        qs = qs.filter(doutorado=True)
    elif modalidade == 'especializacao':
        qs = qs.filter(especializacao=True)

    busca = request.GET.get('q')
    if busca:
        qs = qs.filter(Q(nome__icontains=busca) | Q(sigla__icontains=busca))

    # Limite para performance no mapa
    limit = int(request.GET.get('limit', 5000))
    qs = qs[:limit]

    data = []
    for ies in qs:
        data.append({
            'id': ies.id,
            'sigla': ies.sigla,
            'nome': ies.nome,
            'uf': ies.uf,
            'endereco': ies.endereco,
            'lat': ies.latitude,
            'lng': ies.longitude,
            'homepage': ies.homepage,
            'status': ies.status_juridico,
            'mestrado': ies.mestrado,
            'doutorado': ies.doutorado,
            'especializacao': ies.especializacao,
            'nota_capes': ies.nota_pos_capes,
        })

    return JsonResponse({'ies': data, 'total': len(data)})


def consulta(request):
    """Tabela de consulta com filtros"""
    qs = IES.objects.all()

    # Filtros
    uf = request.GET.get('uf')
    if uf:
        qs = qs.filter(uf=uf)

    status = request.GET.get('status')
    if status:
        qs = qs.filter(status_juridico=status)

    modalidade = request.GET.get('modalidade')
    if modalidade == 'mestrado':
        qs = qs.filter(mestrado=True)
    elif modalidade == 'doutorado':
        qs = qs.filter(doutorado=True)
    elif modalidade == 'especializacao':
        qs = qs.filter(especializacao=True)

    nota_min = request.GET.get('nota_min')
    if nota_min:
        try:
            qs = qs.filter(nota_pos_capes__gte=int(nota_min))
        except ValueError:
            pass

    busca = request.GET.get('q')
    if busca:
        qs = qs.filter(Q(nome__icontains=busca) | Q(sigla__icontains=busca))

    # Paginacao
    paginator = Paginator(qs, 25)
    page = request.GET.get('page', 1)
    ies_list = paginator.get_page(page)

    estados = Estado.objects.all()
    status_list = IES.objects.values_list('status_juridico', flat=True).distinct().order_by('status_juridico')

    context = {
        'ies_list': ies_list,
        'estados': estados,
        'status_list': [s for s in status_list if s],
        'filtros': {
            'uf': uf or '',
            'status': status or '',
            'modalidade': modalidade or '',
            'nota_min': nota_min or '',
            'q': busca or '',
        }
    }
    return render(request, 'ies/consulta.html', context)


def exportar_csv(request):
    """Exporta resultado da consulta como CSV"""
    qs = IES.objects.all()

    # Mesmos filtros da consulta
    uf = request.GET.get('uf')
    if uf:
        qs = qs.filter(uf=uf)
    status = request.GET.get('status')
    if status:
        qs = qs.filter(status_juridico=status)
    busca = request.GET.get('q')
    if busca:
        qs = qs.filter(Q(nome__icontains=busca) | Q(sigla__icontains=busca))

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ies_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Sigla', 'Nome', 'UF', 'Cidade', 'Endereco', 'Status Juridico',
                     'Latitude', 'Longitude', 'Homepage', 'Mestrado', 'Doutorado',
                     'Especializacao', 'Nota CAPES'])

    for ies in qs:
        writer.writerow([
            ies.sigla, ies.nome, ies.uf,
            str(ies.cidade) if ies.cidade else '',
            ies.endereco, ies.status_juridico,
            ies.latitude, ies.longitude, ies.homepage,
            'Sim' if ies.mestrado else 'Nao',
            'Sim' if ies.doutorado else 'Nao',
            'Sim' if ies.especializacao else 'Nao',
            ies.nota_pos_capes or '',
        ])

    return response


def detalhe(request, ies_id):
    """Pagina detalhada de uma IES"""
    ies = get_object_or_404(IES, pk=ies_id)
    cursos = CursoPos.objects.filter(ies=ies)

    # Filtro de cursos por grau
    grau = request.GET.get('grau')
    if grau:
        cursos = cursos.filter(grau=grau)

    context = {
        'ies': ies,
        'cursos': cursos,
    }
    return render(request, 'ies/detalhe.html', context)


def dashboard(request):
    """Pagina com estatisticas e graficos"""
    # IES por UF
    ies_por_uf = (IES.objects
                  .values('uf')
                  .annotate(total=Count('id'))
                  .order_by('-total'))

    # IES por status juridico
    ies_por_status = (IES.objects
                      .values('status_juridico')
                      .annotate(total=Count('id'))
                      .order_by('-total'))

    # Top areas de conhecimento
    top_areas = (IES.objects
                 .exclude(area_conhecimento='')
                 .values('area_conhecimento')
                 .annotate(total=Count('id'))
                 .order_by('-total')[:15])

    # Nota media CAPES por UF (dos cursos, 1-7 reais)
    nota_por_uf = (CursoPos.objects
                   .exclude(conceito__isnull=True)
                   .values('ies__uf')
                   .annotate(media_nota=Avg('conceito'))
                   .order_by('-media_nota'))

    # Cursos por grau
    cursos_por_grau = (CursoPos.objects
                       .values('grau')
                       .annotate(total=Count('id'))
                       .order_by('-total'))

    # Total de IES e cursos
    total_ies = IES.objects.count()
    total_cursos = CursoPos.objects.count()

    total_estados = Estado.objects.values('sigla').distinct().count()

    context = {
        'ies_por_uf': list(ies_por_uf),
        'ies_por_status': list(ies_por_status),
        'top_areas': list(top_areas),
        'nota_por_uf': list(nota_por_uf),
        'cursos_por_grau': list(cursos_por_grau),
        'total_ies': total_ies,
        'total_cursos': total_cursos,
        'total_estados': total_estados,
    }
    return render(request, 'ies/dashboard.html', context)


def api_dashboard(request):
    """API JSON para dados do dashboard"""
    ies_por_uf = list(IES.objects.values('uf').annotate(total=Count('id')).order_by('-total'))
    ies_por_status = list(IES.objects.values('status_juridico').annotate(total=Count('id')).order_by('-total'))
    nota_por_uf = list(CursoPos.objects.exclude(conceito__isnull=True)
                       .values('ies__uf').annotate(media=Avg('conceito')).order_by('-media'))

    return JsonResponse({
        'ies_por_uf': ies_por_uf,
        'ies_por_status': ies_por_status,
        'nota_por_uf': nota_por_uf,
    })
