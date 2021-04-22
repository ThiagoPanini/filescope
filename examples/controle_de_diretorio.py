"""
---------------------------------------------------
----- Exemplos de uso - Controle de diretório -----
---------------------------------------------------
Script responsável por consolidar um exemplo de 
aplicação associado a criação de um report de 
controle de diretório considerando todos os arquivos
presentes em uma determinada origem

Sumário
---------------------------------------------------
1. Configuração inicial
    1.1 Importando bibliotecas
    1.2 Definição de variáveis do projeto
2. Gerando report de controle de diretório
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
from filescope.manager import controle_de_diretorio, generate_visual_report


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
DST_PATH = os.getenv('DST_PATH')
ROOT_FILE = os.path.join(DST_PATH, 'root_control.csv')
OUTPUT_PATH = os.path.join(DST_PATH)


"""
------------------------------------------------------
----- 3. GERANDO REPORT DE CONTROLE DE DIRETÓRIO -----
------------------------------------------------------ 
"""

# Controle de diretório
df_root = controle_de_diretorio(root=SRC_PATH, output_filepath=ROOT_FILE)

# Analisando visualmente o report
generate_visual_report(df=df_root, output_path=OUTPUT_PATH)