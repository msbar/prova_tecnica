# Prova Técnica para Vaga de Engenheiro de Dados

## Objetivo:

* Carga para sqlite dos arquivos públicos das séries históricas dos preços de combustíveis
* Análises estatísticas desta série histórica

Download

## Este projeto foi feito com:

* [Python 3.10.4](https://www.python.org/)
* [Pandas 1.4.3](https://pandas.pydata.org/)
* [SQLModel 0.0.6](https://sqlmodel.tiangolo.com/)



## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode os etl para popular as tabelas

```
git clone https://github.com/msbar/prova_tecnica.git
cd prova_tecnica
python -m venv .venv

# Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt