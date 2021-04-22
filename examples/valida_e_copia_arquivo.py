"""
---------------------------------------------------
- Exemplos de uso - Validação e cópia de arquivos -
---------------------------------------------------
Script responsável por consolidar um exemplo de 
aplicação associado a validação de atualização de
um arquivo em um diretório origem e a subsequente
realização da cópia do mesmo a um diretório destino

Sumário
---------------------------------------------------
1. Configuração inicial
    1.1 Importando bibliotecas
    1.2 Definição de variáveis do projeto
2. Validando e copiando arquivo
---------------------------------------------------
"""

# Autor: Thiago Panini
# Data: 18/04/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÃO INICIAL --------------
           1.1 Importando bibliotecas
---------------------------------------------------
"""

# Bibliotecas padrão
from dotenv import load_dotenv, find_dotenv
import os

# Filescope
from filescope.manager import valida_dt_mod_arquivo, copia_arquivo


"""
------------------------------------------------------
-------------- 1. CONFIGURAÇÃO INICIAL ---------------
        1.2 Definição de variáveis do projeto
------------------------------------------------------ 
"""

# Lendo variáveis de ambiente
load_dotenv(find_dotenv())

# Definindo variáveis de diretório
SRC_PATH = os.getenv('SRC_PATH')
SRC_FILENAME = os.getenv('SRC_FILENAME')
DST_PATH = os.getenv('DST_PATH')
DST_FILENAME = os.getenv('DST_FILENAME')

# Definindo variáveis de validação
JANELA_VALIDA = 'anomesdia'
DT_VALIDA = 20210418


"""
------------------------------------------------------
---------- 2. VALIDANDO E COPIANDO ARQUIVO -----------
------------------------------------------------------ 
"""

# Copiando arquivo em caso de sucesso na validação
if valida_dt_mod_arquivo(dir_origem=SRC_PATH, nome_arquivo=SRC_FILENAME, 
                         janela=JANELA_VALIDA, dt_valida=DT_VALIDA):
    copia_arquivo(origem=os.path.join(SRC_PATH, SRC_FILENAME),
                  destino=os.path.join(DST_PATH, DST_FILENAME))