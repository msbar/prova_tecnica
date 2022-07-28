from sqlmodel import Session

from db import ConnectionHandler
from logger import logger
from models import Produto

log = logger().getLogger(__name__)
db = ConnectionHandler()


def create_produtos():

    p1 = Produto(nome_produto="DIESEL")
    p2 = Produto(nome_produto="DIESEL S10")
    p3 = Produto(nome_produto="ETANOL")
    p4 = Produto(nome_produto="GASOLINA")
    p5 = Produto(nome_produto="GASOLINA ADITIVADA")
    p6 = Produto(nome_produto="GLP")
    p7 = Produto(nome_produto="GNV")

    with Session(db.engine) as session:
        session.add(p1)
        session.add(p2)
        session.add(p3)
        session.add(p4)
        session.add(p5)
        session.add(p6)
        session.add(p7)

        session.commit()


def execute():
    log.info(f'Criando Produtos.')
    create_produtos()
    log.info(f'Produtos criados.')
