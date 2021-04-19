"""
---------------------------------------------------
--------------- TÓPICO: File System ---------------
---------------------------------------------------
Script python responsável por alocar funções úteis
para auxiliar o tratamento e o manuseio de operações
realizadas no sistema operacional, como validação e
cópia de arquivos ou controle e gerenciamento de 
diretórios locais.

Sumário
---------------------------------------------------
1. Configuração Inicial
    1.1 Importando bibliotecas
    1.2 Definindo objetos de log
2. Validação e Manuseio de Arquivos
    2.1 Validação na Origem
    2.2 Cópia de Arquivos
3. Controle de Diretório
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

# Importando bibliotecas
import logging
import os
from os.path import isdir
import shutil
import pandas as pd
from pandas import DataFrame
import time
from datetime import datetime
from pwd import getpwuid


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÃO INICIAL --------------
           1.2 Definindo objetos de log
---------------------------------------------------
"""

def log_config(logger, level=logging.DEBUG, 
               log_format='%(levelname)s;%(asctime)s;%(filename)s;%(module)s;%(lineno)d;%(message)s',
               log_filepath=os.path.join(os.getcwd(), 'exec_log/execution_log.log'),
               flag_file_handler=False, flag_stream_handler=True, filemode='a'):
    """
    Função que recebe um objeto logging e aplica configurações básicas ao mesmo

    Parâmetros
    ----------
    :param logger: objeto logger criado no escopo do módulo [type: logging.getLogger()]
    :param level: level do objeto logger criado [type: level, default: logging.DEBUG]
    :param log_format: formato do log a ser armazenado [type: string]
    :param log_filepath: caminho onde o arquivo .log será armazenado [type: string, default: 'log/application_log.log']
    :param flag_file_handler: flag para salvamento de arquivo .log [type: bool, default=False]
    :param flag_stream_handler: flag para verbosity do log no cmd [type: bool, default=True]
    :param filemode: tipo de escrita no arquivo de log [type: string, default: 'a' (append)]

    Retorno
    -------
    :return logger: objeto logger pré-configurado
    """

    # Setting level for the logger object
    logger.setLevel(level)

    # Creating a formatter
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Creating handlers
    if flag_file_handler:
        log_path = '/'.join(log_filepath.split('/')[:-1])
        if not isdir(log_path):
            makedirs(log_path)

        # Adicionando file_handler
        file_handler = logging.FileHandler(log_filepath, mode=filemode, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if flag_stream_handler:
        # Adicionando stream_handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)    
        logger.addHandler(stream_handler)

    return logger


# Configurando objeto de log
logger = logging.getLogger(__file__)
logger = log_config(logger)


"""
---------------------------------------------------
------- 2. VALIDAÇÃO E MANUSEIO DE ARQUIVOS -------
            2.1 Validação na Origem
---------------------------------------------------
"""

def valida_arquivo_origem(dir_origem, nome_arquivo):
    """
    Função responsável por validar a presença de um arquivo em determinado diretório origem

    Parâmetros
    ----------
    :param dir_origem: caminho do diretório origem alvo da validação [type: string]
    :param nome_arquivo: nome do arquivo (com extensão) a ser validado [type: string]

    Retorno
    -------
    :return flag: flag indicativo da presença do arquivo no diretório origem [type: bool]

    Aplicação
    ---------
    # Verificando arquivo em diretório
    nome_arquivo = 'arquivo.txt'
    origem = 'C://Users/user/Desktop'
    if valida_arquivo_origem(origem=origem, nome_arquivo=nome_arquivo):
        doSomething()
    else:
        doNothing()
    """
    
    # Validando presença do arquivo na origem
    try:
        arquivos_na_origem = os.listdir(path=dir_origem)
        if nome_arquivo in arquivos_na_origem:
            logger.info(f'Arquivo {nome_arquivo} presente na origem {dir_origem}')
            return True
        else:
            logger.warning(f'Arquivo {nome_arquivo} não presente na origem {dir_origem}')
            return False
    except NotADirectoryError as e:
        logger.error(f'Parâmetro origem {dir_origem} não é um diretório de rede. Exception lançada: {e}')
        return False
    except FileNotFoundError as e:
        logger.error(f'Arquivo {nome_arquivo} não encontrado na origem. Exception lançada: {e}')
        return False

def valida_dt_mod_arquivo(dir_origem, nome_arquivo, janela, dt_valida):
    """
    Função responsável por validar a presença e a última data de execução
    de um arquivo em determinado diretório origem e em uma determinada janela
    temporal de modificação

    Parâmetros
    ----------
    :param dir_origem: caminho do diretório origem alvo da validação [type: string]
    :param nome_arquivo: nome do arquivo (com extensão) a ser validado [type: string]
    :param janela: referência sobre janela de validação [type: string, default='anomes']
            *opções: 'ano', 'anomes' ou 'anomesdia'
    :param dt_valida: valor relacionado a janela de validação [type: int, default=int(datetime.now().strftime('%Y%m%d'))]
            *opções: números no fromato 'yyyy', 'yyyyMM' ou 'yyyyMMdd' de acordo com a janela fornecida

    Retorno
    -------
    :return flag: flag indicativo da presença e a atualização do arquivo na origem [type: bool]

    Aplicação
    ---------
    # Verificando arquivo em diretório
    origem = 'C://Users/user/Desktop'
    nome_arquivo = 'arquivo.txt'
    if valida_dt_mod_arquivo(origem=origem, nome_arquivo=nome_arquivo, janela='anomes', dt_valida=202104):
        doSomething()
    else:
        doNothing()
    """

    # Validando janela de validação entre as opções possíveis
    if janela not in ['ano', 'anomes', 'anomesdia']:
        logger.error(f'Janela {janela} inválida. Deve estar entre "ano", "anomes" ou "anomesdia" para validação do arquivo.')
        return

    # Validando tipo primitivo do argumento de validação
    try:
        dt_valida = int(dt_valida)
    except Exception as e:
        logger.error(f'Falha no casting do argumento dt_valida ({dt_valida}) para inteiro. Insira um valor do tipo int para este parâmetro')
        return  

    # Validando sinergia entre os argumentos janela e dt_valida
    qtd_data = len(str(dt_valida))
    if (janela == 'ano' and qtd_data != 4) or (janela == 'anomes' and qtd_data != 6) or (janela == 'anomesdia' == qtd_data != 8):
        logger.error(f'Argumentos "janela" ({janela}) e "dt_valida" ({dt_valida}) não se conversam. Impossível aplicar validação.')
        return

    # Definindo mensagens
    msg_ok = f'A última modificação do arquivo {nome_arquivo} é igual ou superior a do validador ({janela}: {dt_valida})'
    msg_nok = f'A última modificação do arquivo {nome_arquivo} (placeholder) é inferior a do validador ({dt_valida})'

    # Validando presença do arquivo na origem e coletando última data de modificação
    try:
        file_mod_date = os.path.getmtime(os.path.join(dir_origem, nome_arquivo))

        # Janela selecionada: ano
        if janela == 'ano':
            ano_mod = int(time.strftime('%Y', time.localtime(file_mod_date)))
            if dt_valida >= ano_mod:
                logger.info(msg_ok)
                return True
            else:
                logger.warning(msg_nok.replace('placeholder', str(ano_mod)))
                return False

        # Janela selecionada: anomes
        elif janela == 'anomes':
            anomes_mod = int(time.strftime('%Y%m', time.localtime(file_mod_date)))
            if dt_valida >= anomes_mod:
                logger.info(msg_ok)
                return True
            else:
                logger.warning(msg_nok.replace('placeholder', str(anomes_mod)))
                return False

        # Janela selecionada: anomesdida
        elif janela == 'anomesdia':
            anomesdia_mod = int(time.strftime('%Y%m%d', time.localtime(file_mod_date)))
            if dt_valida >= anomesdia_mod:
                logger.info(msg_ok)
                return True
            else:
                logger.warning(msg_nok.replace('placeholder', str(anomesdia_mod)))
                return False     
    except FileNotFoundError as e:
        logger.error(f'Arquivo {nome_arquivo} não encontrado na origem. Exception lançada: {e}')
        return False


"""
---------------------------------------------------
------- 2. VALIDAÇÃO E MANUSEIO DE ARQUIVOS -------
               2.2 Cópia de Arquivos
---------------------------------------------------
"""

def copia_arquivo(origem, destino, valida_presenca=False):
    """
    Função responsável por copiar um arquivo definido em uma origem para um destino

    Parâmetros
    ----------
    :param origem: definição do arquivo origem (caminho + nome do arquivo) [type: string]
    :param destino: definição do destino da cópia (caminho + nome do arquivo) [type: string]
    :param valida_presenca: flag para validar existência do arquivo na origem [type: bool, default=False]

    Retorno
    -------
    None

    Aplicação
    ---------
    # Copiando arquivo
    origem = '/home/user/folder/file.txt'
    destino = '/home/user/new_folder/file.txt'
    copia_arquivo(origem=origem, destino=destino)
    """

    # Extraindo informações de diretório e arquivo
    src_split = os.path.split(origem)
    src_path = src_split[0]
    src_filename = src_split[-1]
    dst_path = os.path.split(destino)[0]

    # Validando presença do arquivo no diretório
    if valida_presenca and not valida_arquivo_origem(dir_origem=src_path, nome_arquivo=src_filename):
        logger.error(f'Arquivo {src_filename} inexistente na origem {src_path}')
        return

    # Verificando se diretório de saída existe
    if not os.path.isdir(dst_path):
        logger.warning(f'Diretório {dst_path} inexistente. Criando diretório no local especificado')
        try:
            os.makedirs(dst_path)
        except Exception as e:
            logger.error(f'Erro ao tentar criar o diretório {dst_path}. Exception lançada: {e}')
            return

    # Verificando se o arquivo está presente na origem
    try:
        shutil.copyfile(src=origem, dst=destino)
        logger.info(f'Cópia realizada com sucesso. Origem: {origem} - Destino: {destino}')
    except Exception as e:
        # Erro ao copiar arquivo pro destino
        logger.warning(f'Falha ao copiar arquivo. Exception lançada: {e}')


"""
---------------------------------------------------
------------ 3. CONTROLE DE DIRETÓRIOS ------------
---------------------------------------------------
"""

def controle_de_diretorio(root, output_filepath=os.path.join(os.getcwd(), 'controle_root.csv')):
    """
    Função responsável por retornar parâmetros de controle de um determinado diretório:
        - Caminho raíz;
        - Nome do arquivo;
        - Data e hora de criação;
        - Data e hora de modificação;
        - Data e hora do último acesso

    Parâmetros
    ----------
    :param root: caminho do diretório a ser analisado [type: string]
    :param output_file: caminho do output em .csv do arquivo gerado [type: string, default: controle_root.csv]

    Retorno
    -------
    :returns root_manager: arquivo salvo na rede com informações do diretório [type: pd.DataFrame]

    Aplicação
    ---------
    root = '/home/user/folder/'
    controle_root = controle_de_diretorio(root=root)
    """

    # Criando DataFrame e listas para armazenar informações
    root_manager = DataFrame()
    all_files = []
    all_sizes = []
    all_cdt = []
    all_mdt = []
    all_adt = []

    # Iterando sobre todos os arquivos do diretório e subdiretórios
    logger.debug('Iterando sobre os arquivos do diretório root')
    for path, _, files in os.walk(root):
        for name in files:
            # Caminho completo do arquivo
            caminho = os.path.join(path, name)

            # Retornando variáveis
            all_files.append(caminho)
            all_sizes.append(os.path.getsize(caminho))
            all_cdt.append(os.path.getctime(caminho))
            all_mdt.append(os.path.getmtime(caminho))
            all_adt.append(os.path.getatime(caminho))

    # Preenchendo DataFrame
    path_splitter = '\\' if caminho.count('\\') >= caminho.count('/') else '/'
    logger.debug('Preenchendo variáveis de controle')
    root_manager['diretorio'] = [os.split(f)[0] for f in all_files]
    root_manager['arquivo'] = [os.split(f)[-1] for f in all_files]
    root_manager['tamanho_kb'] = [size / 1024 for size in all_sizes]
    root_manager['dt_criacao'] = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cdt)) for cdt in all_cdt] 
    root_manager['dt_ult_modif'] = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mdt)) for mdt in all_mdt]
    root_manager['dt_ult_acesso'] = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(adt)) for adt in all_adt]

    # Salvando arquivo gerado
    logger.debug('Salvando arquivo de controle gerado')
    try:
        path_splitter = '\\' if output_filepath.count('\\') >= output_filepath.count('/') else '/'
        output_dir = path_splitter.join(output_filepath.split(path_splitter)[:-1])
        if not isdir(output_dir):
            os.makedirs(output_dir)
        root_manager.to_csv(output_filepath, index=False)
        logger.info(f'Arquivo de controle para o diretório {root} salvo com sucesso')
    except Exception as e:
        logger.error(f'Erro ao salvar arquivo de controle. Exception lançada: {e}')

    return root_manager

def controle_de_diretorio(root, output_filepath=os.path.join(os.getcwd(), 'controle_root.csv'),
                          sort_col='dias_desde_ult_acesso', ascending=False):
    """
    Função responsável por retornar parâmetros de controle de um determinado diretório:
        - Caminho raíz;
        - Nome do arquivo;
        - Data e hora de criação;
        - Data e hora de modificação;
        - Data e hora do último acesso

    Parâmetros
    ----------
    :param root: caminho do diretório a ser analisado [type: string]
    :param output_file: caminho do output em .csv do arquivo gerado [type: string, default: controle_root.csv]

    Retorno
    -------
    :returns root_manager: arquivo salvo na rede com informações do diretório [type: pd.DataFrame]

    Aplicação
    ---------
    root = '/home/user/folder/'
    controle_root = controle_de_diretorio(root=root)
    """

    # Criando DataFrame e listas para armazenar informações
    root_manager = DataFrame()
    all_files = []
    all_sizes = []
    all_cdt = []
    all_mdt = []
    all_adt = []
    all_owners = []

    # Iterando sobre todos os arquivos do diretório e subdiretórios
    logger.debug('Iterando sobre os arquivos do diretório root')
    for path, _, files in os.walk(root):
        for name in files:
            # Caminho completo do arquivo
            caminho = os.path.join(path, name)

            # Retornando variáveis
            all_files.append(caminho)
            all_sizes.append(os.path.getsize(caminho))
            all_cdt.append(os.path.getctime(caminho))
            all_mdt.append(os.path.getmtime(caminho))
            all_adt.append(os.path.getatime(caminho))
            all_owners.append(getpwuid(os.stat(caminho).st_uid).pw_name)

    # Preenchendo DataFrame
    logger.debug('Preenchendo variáveis de controle')
    root_manager['diretorio'] = [os.path.split(f)[0] for f in all_files]
    root_manager['arquivo'] = [os.path.split(f)[-1] for f in all_files]
    root_manager['tamanho_kb'] = [size / 1024 for size in all_sizes]
    root_manager['usuario_owner'] = all_owners
    root_manager['dt_criacao'] = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cdt)) for cdt in all_cdt] 
    root_manager['dt_ult_modif'] = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mdt)) for mdt in all_mdt]
    root_manager['dt_ult_acesso'] = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(adt)) for adt in all_adt]
    root_manager['dt_relatorio'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Construindo indicadores adicionais de utilização
    date_cols = [col for col in root_manager.columns if 'dt_' in col]
    for col in date_cols:
        root_manager[col] = pd.to_datetime(root_manager[col])

    # Idade do arquivo, dias sem modificação e dias desde último acesso
    root_manager['dias_desde_criacao'] = (root_manager['dt_relatorio'] - root_manager['dt_criacao']).dt.days
    root_manager['dias_desde_ult_modif'] = (root_manager['dt_relatorio'] - root_manager['dt_ult_modif']).dt.days
    root_manager['dias_desde_ult_acesso'] = (root_manager['dt_relatorio'] - root_manager['dt_ult_acesso']).dt.days

    # Ordenando colunas e linhas
    order_cols = ['diretorio', 'arquivo', 'tamanho_kb', 'usuario_owner', 'dt_criacao', 'dias_desde_criacao', 
                  'dt_ult_modif', 'dias_desde_ult_modif', 'dt_ult_acesso', 'dias_desde_ult_acesso', 'dt_relatorio']
    root_manager = root_manager.loc[:, order_cols]
    root_manager = root_manager.sort_values(by=sort_col, ascending=ascending)

    # Salvando arquivo gerado
    logger.debug('Salvando arquivo de controle gerado')
    try:
        output_dir = os.path.split(output_filepath)[0]
        if not isdir(output_dir):
            os.makedirs(output_dir)
        root_manager.to_csv(output_filepath, index=False)
        logger.info(f'Arquivo de controle para o diretório {root} salvo com sucesso')
    except Exception as e:
        logger.error(f'Erro ao salvar arquivo de controle. Exception lançada: {e}')

    return root_manager

