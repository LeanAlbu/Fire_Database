from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import connection
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm

from .consultas_especiais import (
    intersecao_municipio_regiao,
    diferenca_municipio_regiao,
    municipios_area_nome,
    satelites_ordenados,
    municipios_com_populacao,
    municipios_com_focoqueimada,
    municipios_populacao_maior_que_qualquer_area_500,
    municipios_populacao_maior_que_todos_area_200,
    municipios_existe_focoqueimada,
    nomes_satelite_unicos,
    agregados_municipio,
)

# === Autenticação ===
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')

        return render(request, 'login.html', {
            'form': form,
            'error': 'Credenciais inválidas'
        })
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # Dados para os cards-resumo
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM queimadas_app_focoqueimada")
        total_focos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM queimadas_app_municipio")
        total_municipios = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM queimadas_app_regiaoimediata")
        total_regioes = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM queimadas_app_satelite")
        total_satelites = cursor.fetchone()[0]
        # Últimos focos
        cursor.execute("""
            SELECT f.id, f.data_hora, f.latitude, f.longitude, f.potencia_rad, m.nome_municipio
            FROM queimadas_app_focoqueimada f
            LEFT JOIN queimadas_app_municipio m ON f.id_municipio_id = m.id
            ORDER BY f.data_hora DESC
            LIMIT 5
        """)
        ultimos_focos = [
            {
                "id": row[0],
                "data_hora": row[1],
                "latitude": row[2],
                "longitude": row[3],
                "potencia_rad": row[4],
                "id_municipio": {"nome_municipio": row[5]} if row[5] else None
            }
            for row in cursor.fetchall()
        ]

    # Dados para os gráficos (mantém como estava)
    regioes_labels = []
    regioes_data = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.nome_regiao, COUNT(f.id)
            FROM queimadas_app_regiaoimediata r
            LEFT JOIN queimadas_app_municipio m ON m.id_regiao_id = r.id
            LEFT JOIN queimadas_app_focoqueimada f ON f.id_municipio_id = m.id
            GROUP BY r.nome_regiao
        """)
        for row in cursor.fetchall():
            regioes_labels.append(row[0])
            regioes_data.append(row[1])

    daily_labels = []
    daily_data = []
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT to_char(data_hora::date, 'DD/MM'), COUNT(*)
            FROM queimadas_app_focoqueimada
            WHERE data_hora >= NOW() - INTERVAL '7 days'
            GROUP BY data_hora::date
            ORDER BY data_hora::date
        """)
        for row in cursor.fetchall():
            daily_labels.append(row[0])
            daily_data.append(row[1])

    # === Consultas Especiais (SQL cru) ===
    context = {
        "total_focos": total_focos,
        "total_municipios": total_municipios,
        "total_regioes": total_regioes,
        "total_satelites": total_satelites,
        "ultimos_focos": ultimos_focos,
        "regioes_labels": regioes_labels,
        "regioes_data": regioes_data,
        "daily_labels": daily_labels,
        "daily_data": daily_data,

        # Consultas Especiais
        "agregados_municipio": agregados_municipio(),
        "municipios_intersecao": intersecao_municipio_regiao(),
        "municipios_diferenca": diferenca_municipio_regiao(),
        "municipios_s_area_nome": municipios_area_nome(),
        "satelites_ordenados": satelites_ordenados(),
        "municipios_populacao_nao_nula": municipios_com_populacao(),
        "municipios_com_foco": municipios_com_focoqueimada(),
        "municipios_any": municipios_populacao_maior_que_qualquer_area_500(),
        "municipios_all": municipios_populacao_maior_que_todos_area_200(),
        "municipios_exists": municipios_existe_focoqueimada(),
        "satelites_unicos": nomes_satelite_unicos(),
    }
    return render(request, 'dashboard.html', context)












@login_required
def limpar_banco(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            tables = [
                "queimadas_app_satelitequeimada",
                "queimadas_app_focoqueimada",
                "queimadas_app_satelite",
                "queimadas_app_municipio",
                "queimadas_app_regiaoimediata"
            ]
            for table in tables:
                cursor.execute(f"DELETE FROM {table};")
        messages.success(request, "Banco de dados limpo com sucesso!")
    return redirect('dashboard')

# === Região Imediata ===
@login_required
def regiao_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, bioma, nome_regiao, clima_regiao
            FROM queimadas_app_regiaoimediata
            ORDER BY nome_regiao ASC
        """)
        regioes = cursor.fetchall()
    return render(request, 'regiao/list.html', {'regioes': regioes})


@login_required
def regiao_create(request):
    if request.method == 'POST':
        form = RegiaoImediataForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO queimadas_app_regiaoimediata (bioma, nome_regiao, clima_regiao)
                    VALUES (%s, %s, %s)
                """, [
                    form.cleaned_data['bioma'],
                    form.cleaned_data['nome_regiao'],
                    form.cleaned_data['clima_regiao']
                ])
            return redirect('regiao_list')
    else:
        form = RegiaoImediataForm()
    return render(request, 'regiao/form.html', {'form': form})


@login_required
def regiao_update(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, bioma, nome_regiao, clima_regiao
            FROM queimadas_app_regiaoimediata
            WHERE id = %s
        """, [pk])
        regiao = cursor.fetchone()

    if request.method == 'POST':
        form = RegiaoImediataForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE queimadas_app_regiaoimediata
                    SET bioma = %s, nome_regiao = %s, clima_regiao = %s
                    WHERE id = %s
                """, [
                    form.cleaned_data['bioma'],
                    form.cleaned_data['nome_regiao'],
                    form.cleaned_data['clima_regiao'],
                    pk
                ])
            return redirect('regiao_list')
    else:
        initial = {
            'bioma': regiao[1],
            'nome_regiao': regiao[2],
            'clima_regiao': regiao[3]
        }
        form = RegiaoImediataForm(initial=initial)
    return render(request, 'regiao/form.html', {'form': form})


@login_required
def regiao_delete(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM queimadas_app_regiaoimediata
                WHERE id = %s
            """, [pk])
        return redirect('regiao_list')
    return render(request, 'regiao/confirm_delete.html', {'pk': pk})


# === Foco de Queimada ===
@login_required
def foco_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                foco.id AS foco_id,
                foco.data_hora,
                foco.latitude,
                foco.longitude,
                foco.potencia_rad,
                municipio.nome_municipio AS nome_municipio,
                satelite.nome_satelite AS nome_satelite
            FROM queimadas_app_focoqueimada AS foco
            JOIN queimadas_app_municipio AS municipio ON foco.id_municipio_id = municipio.id
            LEFT JOIN queimadas_app_satelitequeimada AS sq ON sq.id_queimada_id = foco.id
            LEFT JOIN queimadas_app_satelite AS satelite ON sq.id_satelite_id = satelite.id
            ORDER BY foco.data_hora DESC
        """)
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {"focos": rows}
    return render(request, "foco/list.html", context)

@login_required
def foco_create(request):
    if request.method == 'POST':
        form = FocoQueimadaForm(request.POST)
        if form.is_valid():
            foco = form.save(commit=False)
            foco.save()
            foco.satelites.clear()
            for satelite in form.cleaned_data['satelites']:
                SateliteQueimada.objects.create(id_queimada=foco, id_satelite=satelite)

            return redirect('foco_list')
    else:
        form = FocoQueimadaForm()
    return render(request, 'foco/form.html', {'form': form})


@login_required
def foco_update(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, data_hora, latitude, longitude, potencia_rad, id_municipio_id
            FROM queimadas_app_focoqueimada
            WHERE id = %s
        """, [pk])
        foco = cursor.fetchone()

    if request.method == 'POST':
        form = FocoQueimadaForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE queimadas_app_focoqueimada
                    SET data_hora = %s, latitude = %s, longitude = %s,
                        potencia_rad = %s, id_municipio_id = %s
                    WHERE id = %s
                """, [
                    form.cleaned_data['data_hora'],
                    form.cleaned_data['latitude'],
                    form.cleaned_data['longitude'],
                    form.cleaned_data['potencia_rad'],
                    form.cleaned_data['id_municipio'].id if form.cleaned_data['id_municipio'] else None,
                    pk
                ])
            return redirect('foco_list')
    else:
        form = FocoQueimadaForm(initial={
            'data_hora': foco[1],
            'latitude': foco[2],
            'longitude': foco[3],
            'potencia_rad': foco[4],
            'id_municipio': foco[5]
        })
    return render(request, 'foco/form.html', {'form': form})


@login_required
def foco_delete(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM queimadas_app_focoqueimada
                WHERE id = %s
            """, [pk])
        return redirect('foco_list')
    return render(request, 'foco/confirm_delete.html', {'pk': pk})


# === Município ===
@login_required
def municipio_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                m.id AS municipio_id, 
                m.nome_municipio, 
                m.area_km2, 
                m.populacao, 
                r.nome_regiao AS regiao
            FROM queimadas_app_municipio AS m
            JOIN queimadas_app_regiaoimediata AS r ON m.id_regiao_id = r.id
            ORDER BY m.nome_municipio ASC
        """)
        municipios = cursor.fetchall()
    return render(request, 'municipio/list.html', {'municipios': municipios})


@login_required
def municipio_create(request):
    if request.method == 'POST':
        form = MunicipioForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO queimadas_app_municipio
                    (nome_municipio, area_km2, populacao, id_regiao_id)
                    VALUES (%s, %s, %s, %s)
                """, [
                    form.cleaned_data['nome_municipio'],
                    form.cleaned_data['area_km2'],
                    form.cleaned_data['populacao'],
                    form.cleaned_data['id_regiao'].id
                ])
            return redirect('municipio_list')
    else:
        form = MunicipioForm()
    return render(request, 'municipio/form.html', {'form': form})


@login_required
def municipio_update(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome_municipio, area_km2, populacao, id_regiao_id
            FROM queimadas_app_municipio
            WHERE id = %s
        """, [pk])
        municipio = cursor.fetchone()

    if request.method == 'POST':
        form = MunicipioForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE queimadas_app_municipio
                    SET nome_municipio = %s, area_km2 = %s, populacao = %s, id_regiao_id = %s
                    WHERE id = %s
                """, [
                    form.cleaned_data['nome_municipio'],
                    form.cleaned_data['area_km2'],
                    form.cleaned_data['populacao'],
                    form.cleaned_data['id_regiao'].id,
                    pk
                ])
            return redirect('municipio_list')
    else:
        form = MunicipioForm(initial={
            'nome_municipio': municipio[1],
            'area_km2': municipio[2],
            'populacao': municipio[3],
            'id_regiao': municipio[4]
        })
    return render(request, 'municipio/form.html', {'form': form})


@login_required
def municipio_delete(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM queimadas_app_municipio
                WHERE id = %s
            """, [pk])
        return redirect('municipio_list')
    return render(request, 'municipio/confirm_delete.html', {'pk': pk})


# === Satélite ===
@login_required
def satelite_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome_satelite, pais_origem, tipo_orbita
            FROM queimadas_app_satelite
            ORDER BY nome_satelite ASC
        """)
        satelites = cursor.fetchall()
    return render(request, 'satelite/list.html', {'satelites': satelites})


@login_required
def satelite_create(request):
    if request.method == 'POST':
        form = SateliteForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO queimadas_app_satelite (nome_satelite, pais_origem, tipo_orbita)
                    VALUES (%s, %s, %s)
                """, [
                    form.cleaned_data['nome_satelite'],
                    form.cleaned_data['pais_origem'],
                    form.cleaned_data['tipo_orbita']
                ])
            return redirect('satelite_list')
    else:
        form = SateliteForm()
    return render(request, 'satelite/form.html', {'form': form})


@login_required
def satelite_update(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome_satelite, pais_origem, tipo_orbita
            FROM queimadas_app_satelite
            WHERE id = %s
        """, [pk])
        satelite = cursor.fetchone()

    if request.method == 'POST':
        form = SateliteForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE queimadas_app_satelite
                    SET nome_satelite = %s, pais_origem = %s, tipo_orbita = %s
                    WHERE id = %s
                """, [
                    form.cleaned_data['nome_satelite'],
                    form.cleaned_data['pais_origem'],
                    form.cleaned_data['tipo_orbita'],
                    pk
                ])
            return redirect('satelite_list')
    else:
        form = SateliteForm(initial={
            'nome_satelite': satelite[1],
            'pais_origem': satelite[2],
            'tipo_orbita': satelite[3]
        })
    return render(request, 'satelite/form.html', {'form': form})


@login_required
def satelite_delete(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM queimadas_app_satelite
                WHERE id = %s
            """, [pk])
        return redirect('satelite_list')
    return render(request, 'satelite/confirm_delete.html', {'pk': pk})


# === CONSULTAS ESPECIAIS SQL CRU ===

@login_required
def consulta_intersecao(request):
    resultado = intersecao_municipio_regiao()
    return render(request, 'consultas/intersecao.html', {'resultado': resultado})

@login_required
def consulta_diferenca(request):
    resultado = diferenca_municipio_regiao()
    return render(request, 'consultas/diferenca.html', {'resultado': resultado})

@login_required
def consulta_between_like(request):
    resultado = municipios_area_nome()
    return render(request, 'consultas/between_like.html', {'resultado': resultado})

@login_required
def consulta_order_by(request):
    resultado = satelites_ordenados()
    return render(request, 'consultas/order_by.html', {'resultado': resultado})

@login_required
def consulta_is_not_null(request):
    resultado = municipios_com_populacao()
    return render(request, 'consultas/is_not_null.html', {'resultado': resultado})

@login_required
def consulta_in(request):
    resultado = municipios_com_focoqueimada()
    return render(request, 'consultas/in.html', {'resultado': resultado})

@login_required
def consulta_any(request):
    resultado = municipios_populacao_maior_que_qualquer_area_500()
    return render(request, 'consultas/any.html', {'resultado': resultado})

@login_required
def consulta_all(request):
    resultado = municipios_populacao_maior_que_todos_area_200()
    return render(request, 'consultas/all.html', {'resultado': resultado})

@login_required
def consulta_exists(request):
    resultado = municipios_existe_focoqueimada()
    return render(request, 'consultas/exists.html', {'resultado': resultado})

@login_required
def consulta_unique(request):
    resultado = nomes_satelite_unicos()
    return render(request, 'consultas/unique.html', {'resultado': resultado})

@login_required
def consulta_agregacao(request):
    resultado = agregados_municipio()
    return render(request, 'consultas/agregacao.html', {'resultado': resultado})
