from django.db import connection

def intersecao_municipio_regiao():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nome_municipio FROM queimadas_app_municipio
            INTERSECT
            SELECT nome_regiao FROM queimadas_app_regiaoimediata;
        """)
        return [row[0] for row in cursor.fetchall()]

def diferenca_municipio_regiao():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nome_municipio FROM queimadas_app_municipio
            EXCEPT
            SELECT nome_regiao FROM queimadas_app_regiaoimediata;
        """)
        return [row[0] for row in cursor.fetchall()]

def municipios_area_nome():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nome_municipio, area_km2
            FROM queimadas_app_municipio
            WHERE area_km2 BETWEEN 100 AND 500
            AND nome_municipio LIKE 'S%';
        """)
        return cursor.fetchall()

def satelites_ordenados():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nome_satelite, pais_origem
            FROM queimadas_app_satelite
            ORDER BY nome_satelite ASC, pais_origem DESC;
        """)
        return cursor.fetchall()

def municipios_com_populacao():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nome_municipio
            FROM queimadas_app_municipio
            WHERE populacao IS NOT NULL;
        """)
        return [row[0] for row in cursor.fetchall()]

def municipios_com_focoqueimada():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nome_municipio
            FROM queimadas_app_municipio
            WHERE id IN (SELECT id_municipio_id FROM queimadas_app_focoqueimada);
        """)
        return [row[0] for row in cursor.fetchall()]

def municipios_populacao_maior_que_qualquer_area_500():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nome_municipio
            FROM queimadas_app_municipio
            WHERE populacao > ANY (
                SELECT populacao
                FROM queimadas_app_municipio
                WHERE area_km2 > 500
            );
        """)
        return [row[0] for row in cursor.fetchall()]

def municipios_populacao_maior_que_todos_area_200():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nome_municipio
            FROM queimadas_app_municipio
            WHERE populacao > ALL (
                SELECT populacao
                FROM queimadas_app_municipio
                WHERE area_km2 < 200
            );
        """)
        return [row[0] for row in cursor.fetchall()]

def municipios_existe_focoqueimada():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nome_municipio
            FROM queimadas_app_municipio m
            WHERE EXISTS (
                SELECT 1
                FROM queimadas_app_focoqueimada f
                WHERE f.id_municipio_id = m.id
            );
        """)
        return [row[0] for row in cursor.fetchall()]

def nomes_satelite_unicos():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT nome_satelite
            FROM queimadas_app_satelite;
        """)
        return [row[0] for row in cursor.fetchall()]

def agregados_municipio():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                AVG(populacao) AS media_populacao,
                MIN(area_km2) AS menor_area,
                MAX(area_km2) AS maior_area,
                SUM(populacao) AS soma_populacao,
                COUNT(*) AS total_municipios
            FROM queimadas_app_municipio;
        """)
        row = cursor.fetchone()
        return {
            "media_populacao": row[0],
            "menor_area": row[1],
            "maior_area": row[2],
            "soma_populacao": row[3],
            "total_municipios": row[4]
        }
