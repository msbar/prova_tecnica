import datetime
from typing import Optional

from pydantic import condecimal
from sqlmodel import Field, SQLModel


class Estabelecimento(SQLModel, table=True):
    cnpj_completo: str = Field(primary_key=True)
    cnpj_basico: str
    revenda: str
    regiao_sigla: str
    estado_sigla: str
    municipio: str
    rua: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None


class Produto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome_produto: str


class Preco(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cnpj_completo: str
    produto_id: int
    data_coleta: datetime.date
    valor_venda: condecimal(max_digits=18, decimal_places=3) = Field(default=None)
    valor_compra: condecimal(max_digits=18, decimal_places=3) = Field(default=None)
    unidade_de_medida: str
    bandeira: str
