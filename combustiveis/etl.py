from db import ConnectionHandler
from estabelecimentos import execute as estabelecimento_execute
from logger import logger
from precos import execute as preco_execute
from produtos import execute as prod_execute

log = logger().getLogger(__name__)

log.info(f'Criando banco de dados e tabelas')
db = ConnectionHandler()
db.create_db_and_tables()

log.info(f'Inserindo Produtos')
prod_execute()

log.info(f'Inserindo Estabelecimentos')
estabelecimento_execute()

log.info(f'Inserindo Preços')
preco_execute()
