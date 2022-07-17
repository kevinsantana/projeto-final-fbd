import pandas


def municipio(csv: str):
    estados = {
        "ACRE": 1,
        "ALAGOAS": 2,
        "AMAZONAS": 3,
        "AMAPÁ": 4,
        "BAHIA": 5,
        "CEARÁ": 6,
        "DISTRITO FEDERAL": 7,
        "ESPÍRITO SANTO": 8,
        "GOIÁS": 9,
        "MARANHÃO": 10,
        "MINAS GERAIS": 11,
        "MATO GROSSO DO SUL": 12,
        "MATO GROSSO": 13,
        "PARÁ": 14,
        "PARAÍBA": 15,
        "PERNAMBUCO": 16,
        "PIAUÍ": 17,
        "PARANÁ": 18,
        "RIO DE JANEIRO": 19,
        "RIO GRANDE DO NORTE": 20,
        "RONDÔNIA": 21,
        "RORAIMA": 22,
        "RIO GRANDE DO SUL": 23,
        "SANTA CATARINA": 24,
        "SERGIPE": 25,
        "SÃO PAULO": 26,
        "TOCANTINS": 27,
    }
    municipio_query = "INSERT INTO public.MUNICIPIO (CODIGO_IBGE, MUNICIPIO_NOME, ESTADO_ID_ESTADO) VALUES ('{ibge}', $${municipio}$$, {estado})"
    linhas = pandas.read_excel(
        csv, usecols=["Nome_UF", "Código Município Completo", "Nome_Município"]
    )
    try:
        queries = open("/media/rebellion/LORDS_BLADE/python/mestrado/fbd/queries_municipio.txt", "w")
        linhas = linhas.to_dict(orient="records")
        for i in range(len(linhas) - 1):
            atual, proximo = linhas[i], linhas[i+1]
            if atual != proximo:
                uf, ibge, nm_mun = linhas[i].values()
                uf_id = estados.get(uf.upper().strip())
                query = municipio_query.format(ibge=ibge, municipio=nm_mun, estado=uf_id)
                queries.write(query +  ";" + "\n")
            else:
                print(atual)
                print(proximo)
    finally:
        queries.close()


if __name__ == "__main__":
    csv = "/media/rebellion/LORDS_BLADE/python/mestrado/fbd/DTB_2021/RELATORIO_DTB_BRASIL_DISTRITO.ods"
    municipio(csv)
