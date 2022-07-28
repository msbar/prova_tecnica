import logging
import sys


def logger():
    """ Configura o loggin python para a aplicação"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        stream=sys.stdout,
        encoding='UTF-8'
    )
    return logging
