import math
import re

import pandas as pd
from sqlalchemy import select
from sqlmodel import Session

from db import ConnectionHandler
from file_handler import FilesHandler
from logger import logger
from models import Estabelecimento

log = logger().getLogger(__name__)
db = ConnectionHandler()
fh = FilesHandler('datafiles')
files_list = fh.get_files_list()


def create_df(file):
    names = [
        'regiao_sigla',
        'estado_sigla',
        'municipio',
        'revenda',
        'cnpj_revenda',
        'rua',
        'numero',
        'complemento',
        'bairro',
        'cep',
        'produto',
        'data_coleta',
        'valor_venda',
        'valor_compra',
        'unidade_de_medida',
        'bandeira'
    ]

    df = pd.read_csv(
        file,
        sep=';',
        header=1,
        quotechar='"',
        encoding='UTF-8',
        names=names
    )
    return df


def check_estabelecimento_exists(value):
    with Session(db.engine) as session:
        statement = select(Estabelecimento).where(Estabelecimento.cnpj_completo == value)
        results = session.exec(statement)
        r = results.first()

    return True if r else False


def remove_duplicados(df):
    """Remove do dataframe as linhas duplicadas e os já inseridos no banco"""
    df.drop_duplicates(subset=['cnpj_completo'], inplace=True)
    for i in df.index:
        if check_estabelecimento_exists(df['cnpj_completo'][i]):
            df.drop(df[df['cnpj_completo'] == df['cnpj_completo'][i]].index, inplace=True)
    return df


def data_transformer(df):
    # Adiconada a na primeira posição o cnpj_completo
    value = df.cnpj_revenda.apply(lambda x: ''.join(re.findall(r'\d+', x)))
    df.insert(loc=0, column='cnpj_completo', value=value)

    # Adiconada a na segunda posição o cnpj_básico
    value = df.cnpj_completo.apply(lambda x: x[0:8])
    df.insert(loc=1, column='cnpj_basico', value=value)

    df.drop(
        columns=[
            'cnpj_revenda',
            'produto',
            'data_coleta',
            'valor_venda',
            'valor_compra',
            'unidade_de_medida',
            'bandeira'
        ],
        inplace=True
    )
    return df


def insert_db(df):
    table = 'estabelecimento'
    chunksize = math.floor(2097/len(df.columns))
    chunksize = 1000 if chunksize > 1000 else chunksize
    df.to_sql(table, con=db.engine, index=False, method='multi',
              chunksize=chunksize, if_exists='append')


def execute():
    for file in files_list:
        log.info(f'Criando DataFrame para o arquivo {file}.')
        df = create_df(file=file)

        log.info(f'Transformando os dados.')
        df = data_transformer(df)

        log.info(f'Remove Duplicados os dados.')
        df = remove_duplicados(df)

        log.info(f'Inserindo registros no Banco de Dados.')
        insert_db(df)

        log.info(f'Registros inseridos no Banco de Dados.')
