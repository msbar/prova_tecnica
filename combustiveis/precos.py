import math
import re

import pandas as pd

from converters import convert_str_to_float
from db import ConnectionHandler
from file_handler import FilesHandler
from logger import logger
from models import Preco

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
        names=names,
        converters={
            'valor_venda': convert_str_to_float,
            'valor_compra': convert_str_to_float,
        },
    )
    return df


def data_transformer(df):

    # Adicona na primeira posição o cnpj_completo
    value = df.cnpj_revenda.apply(lambda x: ''.join(re.findall(r'\d+', x)))
    df.insert(loc=0, column='cnpj_completo', value=value)

    # Adicona na segunda posição o produto_id
    PRODUTO_ID_DICT = {
        'DIESEL': 1,
        'DIESEL S10': 2,
        'ETANOL': 3,
        'GASOLINA': 4,
        'GASOLINA ADITIVADA': 5,
        'GLP': 6,
        'GNV': 7
    }

    value = df.produto.apply(lambda x: PRODUTO_ID_DICT.get(x))
    df.insert(loc=0, column='produto_id', value=value)

    df.drop(
        columns=[
            'cnpj_revenda',
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
            'produto'
        ],
        inplace=True
    )
    return df


def insert_db(df):
    table = 'preco'
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

        log.info(f'Inserindo registros no Banco de Dados.')
        insert_db(df)

        log.info(f'Registros inseridos no Banco de Dados.')
