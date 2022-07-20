from decimal import Decimal

import numpy
import pandas
from loguru import logger
from alive_progress import alive_bar

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import DictCursor
from psycopg2.extensions import parse_dsn

from projeto_final_fbd.config import envs


def clean_data(linha: dict) -> dict:
    nis_beneficiario, nis_responsavel, nome_responsavel, obs = None, None, None, None
    enquadramento, valor_beneficio = "", ""

    if linha.get("NIS BENEFICI�RIO", None):
        if linha.get("NIS BENEFICI�RIO", None) != "0":
            nis_beneficiario = linha.get("NIS BENEFICI�RIO")
    if linha.get("NIS RESPONS�VEL", None):
        if linha.get("NIS RESPONS�VEL") != -2:
            nis_responsavel = linha.get("NIS RESPONS�VEL")
    if linha.get("NOME RESPONS�VEL", None):
        if linha.get("NOME RESPONS�VEL") != "N�o se aplica":
            nome_responsavel = linha.get("NOME RESPONS�VEL")
    if linha.get("OBSERVA��O", None):
        if linha.get("OBSERVA��O") != "N�o h�":
            obs = linha.get("OBSERVA��O")
        if linha.get("OBSERVA��O") in "Valor devolvido � Uni�o.":
            obs = "Valor devolvido a uniao"
    if linha.get("ENQUADRAMENTO") == "BOLSA FAMILIA":
        enquadramento = "BOLSA_FAMILIA"
    else:
        enquadramento = linha.get("ENQUADRAMENTO")
    if linha.get("VALOR BENEF�CIO"):
        if "," in linha.get("VALOR BENEF�CIO"):
            valor_beneficio = linha.get("VALOR BENEF�CIO").strip().replace(",", ".")
        else:
            valor_beneficio = linha.get("VALOR BENEF�CIO")

    return {
        "CODIGO MUNICIPIO": linha.get("C�DIGO MUNIC�PIO IBGE").strip(),
        "NIS BENEFICIARIO": nis_beneficiario,
        "NOME BENEFICIARIO": linha.get("NOME BENEFICI�RIO").strip(),
        "NIS REPONSAVEL": nis_responsavel,
        "NOME RESPONSAVEL": nome_responsavel,
        "ENQUADRAMENTO": enquadramento.strip(),
        "PARCELA": linha.get("PARCELA").strip()[0],
        "OBSERVACAO": obs,
        "VALOR BENEFICIO": Decimal("{0:.2f}".format(Decimal(valor_beneficio))),
        "MES DISPONIBILIZACAO": "202009",
    }


def insert_beneficio(cursor, conn, dados_beneficio: dict):
    cursor.execute(
        """
        INSERT INTO public.BENEFICIO (CIDADAO_ID_CIDADAO, MUNICIPIO_ID_MUNICIPIO,
        MES_DISPONIBILIZACAO, ENQUADRAMENTO, PARCELA, OBSERVACAO, VALOR_BENEFICIO)
        VALUES (%(cidadao_id_cidadao)s, %(municipio_id_municipio)s, %(mes_disponibilizacao)s,
        %(enquadramento)s, %(parcela)s, %(observacao)s, %(valor_beneficio)s) RETURNING ID_BENEFICIO
        """,
        dados_beneficio,
    )
    conn.commit()
    return True if cursor.fetchone()["id_beneficio"] else False


def insert_cidadao(cursor, conn, dados_cidadao: dict) -> int:
    cursor.execute(
        """
        INSERT INTO public.CIDADAO (CIDADAO_NOME, CIDADAO_NIS, RESPONSAVEL_ID_RESPONSAVEL)
        VALUES (%(cidadao_nome)s, %(cidadao_nis)s, %(responsavel_id_responsavel)s) RETURNING ID_CIDADAO;
        """,
        dados_cidadao,
    )
    conn.commit()
    return cursor.fetchone()["id_cidadao"]


def insert_responsavel(cursor, conn, dados_responsavel: dict) -> int:
    cursor.execute(
        """
        INSERT INTO public.RESPONSAVEL (RESPONSAVEL_NOME, RESPONSAVEL_NIS) 
        VALUES (%(responsavel_nome)s, %(responsavel_nis)s) RETURNING ID_RESPONSAVEL;
        """,
        dados_responsavel,
    )
    conn.commit()
    return cursor.fetchone()["id_responsavel"]


def get_codigo_municipio(cursor, dados_municipio: dict) -> int:
    cursor.execute(
        """
        SELECT ID_MUNICIPIO FROM MUNICIPIO
        WHERE CODIGO_IBGE = %(codigo_ibge)s
        """,
        dados_municipio,
    )
    total = cursor.rowcount
    result = cursor.fetchone()["id_municipio"] if total else None
    return result


def connect_db():
    while True:
        try:
            connection = psycopg2.connect(**parse_dsn(envs.DB_URI))
            if connection:
                cursor = connection.cursor(cursor_factory=DictCursor)
                return cursor, connection
        except OperationalError as op_error:
            logger.error(f"Falha na conexão com o o banco de dados: {op_error}")
            continue


def disconnect_db(cursor, connection):
    cursor.close()
    connection.close()


def make_df(csv: str, n_rows: int = 0, skip_rows: int = 0):
    columns_names = [
        "M�S DISPONIBILIZA��O",
        "UF",
        "C�DIGO MUNIC�PIO IBGE",
        "NOME MUNIC�PIO",
        "NIS BENEFICI�RIO",
        "CPF BENEFICI�RIO",
        "NOME BENEFICI�RIO",
        "NIS RESPONS�VEL",
        "CPF RESPONS�VEL",
        "NOME RESPONS�VEL",
        "ENQUADRAMENTO",
        "PARCELA",
        "OBSERVA��O",
        "VALOR BENEF�CIO"
    ]
    linhas = pandas.read_csv(
        csv,
        sep=";",
        encoding="utf_8",
        encoding_errors="replace",
        usecols=[
            "C�DIGO MUNIC�PIO IBGE",
            "NIS BENEFICI�RIO",
            "NOME BENEFICI�RIO",
            "NIS RESPONS�VEL",
            "NOME RESPONS�VEL",
            "ENQUADRAMENTO",
            "PARCELA",
            "OBSERVA��O",
            "VALOR BENEF�CIO"
        ],
        dtype={
            "C�DIGO MUNIC�PIO IBGE": object,
            "NIS BENEFICI�RIO": object,
            "OBSERVA��O": object,
            "PARCELA": object,
            "VALOR BENEF�CIO": object,
        },
        skiprows=skip_rows,
        engine="c",
        header=0,
        names=columns_names,
        low_memory=True,
        nrows=n_rows,
    )
    linhas = linhas.replace({numpy.nan: None})
    return linhas.to_dict(orient="records")[32:]


def insert_etl(csv: str):
    linhas = make_df(csv, 9_000_000, 18_000_000)
    total = len(linhas)

    with alive_bar(total) as bar:
        for linha in linhas:
            linha_ok = clean_data(linha)
            id_responsavel = None
            cur, conn = connect_db()
            if linha_ok.get("NOME RESPONSAVEL"):
                id_responsavel = insert_responsavel(
                    cur,
                    conn,
                    {
                        "responsavel_nome": linha_ok.get("NOME RESPONSAVEL"),
                        "responsavel_nis": linha_ok.get("NIS REPONSAVEL"),
                    },
                )
            else:
                logger.log("NOME RESPONSAVEL", "Responsavel vazio ou não existe")

            id_cidadao = None
            dados_municipio = {"codigo_ibge": linha_ok.get("CODIGO MUNICIPIO")}
            id_municipio = get_codigo_municipio(cur, dados_municipio)
            if not id_municipio:
                logger.log("CODIGO MUNICIPIO", f"Erro ao buscar municipio: {dados_municipio}")
                continue

            if linha_ok.get("NOME BENEFICIARIO"):
                id_cidadao = insert_cidadao(
                    cur,
                    conn,
                    {
                        "cidadao_nome": linha_ok.get("NOME BENEFICIARIO"),
                        "cidadao_nis": linha_ok.get("NIS BENEFICIARIO"),
                        "responsavel_id_responsavel": id_responsavel,
                    },
                )
            else:
                logger.log("NOME BENEFICIARIO", "Nome do responsável vazio ou não existe")

            dados_beneficio = {
                "cidadao_id_cidadao": id_cidadao,
                "municipio_id_municipio": id_municipio,
                "mes_disponibilizacao": linha_ok.get("MES DISPONIBILIZACAO"),
                "enquadramento": linha_ok.get("ENQUADRAMENTO"),
                "parcela": linha_ok.get("PARCELA"),
                "observacao": linha_ok.get("OBSERVACAO"),
                "valor_beneficio": linha_ok.get("VALOR BENEFICIO"),
            }
            beneficio_ok = insert_beneficio(
                cur,
                conn,
                dados_beneficio,
            )
            if beneficio_ok:
                logger.info("Inserção realizada com sucesso")
            else:
                logger.log("BENEFICIARIO", f"Falha na inserção do benefício: {dados_beneficio}")

            bar()
        disconnect_db(cur, conn)


if __name__ == "__main__":
    csv = "/home/rebellion/FBD/202009_AuxilioEmergencial.csv"
    insert_etl(csv)
