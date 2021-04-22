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
import matplotlib.pyplot as plt 
from matplotlib.gridspec import GridSpec
import seaborn as sns
from warnings import filterwarnings
filterwarnings('ignore')


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÃO INICIAL --------------
  1.2 Definindo de log e salvamento de arquivos
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


def save_data(data, output_path, filename):
    """
    Método responsável por salvar objetos DataFrame em formato csv.

    Parâmetros
    ----------
    :param data: arquivo/objeto a ser salvo [type: pd.DataFrame]
    :param output_path: referência de diretório destino [type: string]
    :param filename: referência do nome do arquivo a ser salvo [type: string]

    Retorno
    -------
    Este método não retorna nenhum parâmetro além do arquivo devidamente salvo no diretório

    Aplicação
    ---------
    df = file_generator_method()
    save_result(df, output_path=OUTPUT_PATH, filename='arquivo.csv')
    """

    # Verificando se diretório existe
    if not os.path.isdir(output_path):
        logger.warning(f'Diretório {output_path} inexistente. Criando diretório no local especificado')
        try:
            os.makedirs(output_path)
        except Exception as e:
            logger.error(f'Erro ao tentar criar o diretório {output_path}. Exception lançada: {e}')
            return

    logger.debug(f'Salvando arquivo no diretório especificado')
    try:
        output_file = os.path.join(output_path, filename)
        data.to_csv(output_file, index=False)
    except Exception as e:
        logger.error(f'Erro ao salvar arquivo {filename}. Exception lançada: {e}')


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
        3.1 Visão analítica de diretório
---------------------------------------------------
"""

# Função para cálculo do score filescope
def calc_filescope_score(df, peso_tkb=2, peso_ddc=1, peso_dda=2, peso_ddm=1):
    """
    Função responsável por calcular o score filescope baseado em pesos e normalização
    
    Parâmetros
    ----------
    :param df: report gerado a partir de função controle_de_diretorio() [type: pd.DataFrame]
    :param peso_tkb: peso do cálculo para o tamanho do arquivo [type: int, default=2]
    :param peso_ddc: peso do cálculo para dias desde a criação [type: int, default=1]
    :param peso_dda: peso do cálculo para dias do último acesso [type: int, default=2]
    :param peso_ddm: peso do cálculo para dias da última modificação [type: int, default=1]
    
    Retorno
    -------
    :return df: base de dados com score filescope calculado [type: pd.DataFrame]
    """
    
    # Dropando coluna de score caso existente
    if 'filescope_score' in df.columns:
        df.drop('filescope_score', axis=1, inplace=True)
    
    # Normalizando colunas numéricas
    num_cols = ['tamanho_kb', 'dias_desde_criacao', 'dias_desde_ult_modif', 'dias_desde_ult_acesso']
    key_cols = ['diretorio', 'arquivo']
    df_score = df.loc[:, key_cols + num_cols]
    for col in num_cols:
        col_max = df_score[col].max()
        col_min = df_score[col].min()
        df_score[col] = (df_score[col] - col_min) / (col_max - col_min)

    # Calculando score filescope a partir de pesos pré definidos
    tkb = peso_tkb * df_score['tamanho_kb']
    ddc = peso_ddc * df_score['dias_desde_criacao'] 
    dda = peso_dda * df_score['dias_desde_ult_acesso']
    ddm = peso_ddm * df_score['dias_desde_ult_modif']
    pesos = peso_tkb * peso_ddc * peso_dda * peso_ddm

    df_score['filescope_score'] = (tkb * ddc * dda * ddm) / pesos

    # Normalizando score
    score_max = df_score['filescope_score'].max()
    score_min = df_score['filescope_score'].min()
    df_score['filescope_score'] = 100 * (df_score['filescope_score'] - score_min) / (score_max - score_min)
    df_score = df_score.loc[:, key_cols + ['filescope_score']]

    # Juntando bases
    return df.merge(df_score, how='left', on=key_cols)

# Gerando report de controle de diretório   
def controle_de_diretorio(root, sort_col='filescope_score', ascending=False, **kwargs):
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
    :param sort_col: coluna de ordenação do report [type: string, default=filescope_score]
    :param ascending: flag para ordenação ascendente [type: bool, flag=False]

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
    root_manager['tamanho_kb'] = [size / 1000 for size in all_sizes]
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
    
    # Enriquecendo base com score filescope
    root_manager = calc_filescope_score(df=root_manager)

    # Ordenando colunas e linhas
    order_cols = ['diretorio', 'arquivo', 'tamanho_kb', 'usuario_owner', 'dt_criacao', 'dias_desde_criacao', 
                  'dt_ult_modif', 'dias_desde_ult_modif', 'dt_ult_acesso', 'dias_desde_ult_acesso', 'filescope_score',
                  'dt_relatorio']
    root_manager = root_manager.loc[:, order_cols]
    root_manager = root_manager.sort_values(by=sort_col, ascending=ascending)

    # Validando salvamento dos resultados
    if 'save' in kwargs and bool(kwargs['save']):
        output_path = kwargs['output_path'] if 'output_path' in kwargs else os.path.join(os.getcwd(), 'output')
        output_filename = kwargs['output_filename'] if 'output_filename' in kwargs else 'controle_diretorio.csv'
        save_data(root_manager, output_path=output_path, filename=output_filename)

    """# Salvando arquivo gerado
    if 'save' in kwargs and bool(kwargs['save']):
        logger.debug('Salvando arquivo de controle gerado')
        output_filepath=os.path.join(os.getcwd(), 'controle_root.csv')
        try:
            output_dir = os.path.split(output_filepath)[0]
            if not isdir(output_dir):
                os.makedirs(output_dir)
            root_manager.to_csv(output_filepath, index=False)
            logger.info(f'Arquivo de controle para o diretório {root} salvo com sucesso')
        except Exception as e:
            logger.error(f'Erro ao salvar arquivo de controle. Exception lançada: {e}')"""

    return root_manager


"""
---------------------------------------------------
------------ 3. CONTROLE DE DIRETÓRIOS ------------
         3.2 Report visual de diretórios
---------------------------------------------------
"""

# Formatando eixos do matplotlib
def format_spines(ax, right_border=False):
    """
    Função responsável por modificar as bordas e cores de eixos do matplotlib

    Parâmetros
    ----------
    :param ax: eixo do gráfico criado no matplotlib [type: matplotlib.pyplot.axes]
    :param right_border: flag para plotagem ou ocultação da borda direita [type: bool, default=True]

    Retorno
    -------
    Esta função não retorna nenhum parâmetro além do eixo devidamente customizado

    Aplicação
    ---------
    fig, ax = plt.subplots()
    format_spines(ax=ax, right_border=False)
    """

    # Definindo cores dos eixos
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['top'].set_visible(False)

    # Validando plotagem da borda direita
    if right_border:
        ax.spines['right'].set_color('black')
    else:
        ax.spines['right'].set_color('#FFFFFF')
    ax.patch.set_facecolor('#FFFFFF')

# Função para conversão de um tamanho em kb para a escala adequada
def convert_kb_into_str(size):
    """
    Converte um parâmetro de tamanho de arquivos (em kb) para a escala mais adequada
    
    Parâmetros
    ----------
    :param size: variável numérica representando o tamanho de arquivos em kb [type: float]
    
    Retorno
    -------
    :param size: valor convertido pra escala mais adequada com o indicativo em str [type: str]
    
    """
    
    # Aplicando regras de conversão
    if size > 1000000:
        size = str(round(size / 1000000, 2)) + ' GB'
    elif size > 1000:
        size = str(round(size / 1000, 2)) + ' MB'
    else:
        size = str(round(size, 2)) + ' KB'
    
    return size

# Função responsável por salvar imagens em formato png
def save_fig(fig, output_path, img_name, tight_layout=True, dpi=300):
    """
    Método responsável por salvar imagens geradas pelo matplotlib/seaborn

    Parâmetros
    ----------
    :param fig: figura criada pelo matplotlib para a plotagem gráfica [type: plt.figure]
    :param output_file: caminho final a ser salvo (+ nome do arquivo em formato png) [type: string]
    :param tight_layout: flag que define o acerto da imagem [type: bool, default=True]
    :param dpi: resolução da imagem a ser salva [type: int, default=300]

    Retorno
    -------
    Este método não retorna nenhum parâmetro além do salvamento da imagem em diretório especificado

    Aplicação
    ---------
    fig, ax = plt.subplots()
    save_fig(fig, output_file='imagem.png')
    """

    # Verificando se diretório existe
    if not os.path.isdir(output_path):
        logger.warning(f'Diretório {output_path} inexistente. Criando diretório no local especificado')
        try:
            os.makedirs(output_path)
        except Exception as e:
            logger.error(f'Erro ao tentar criar o diretório {output_path}. Exception lançada: {e}')
    
    # Acertando layout da imagem
    if tight_layout:
        fig.tight_layout()
    
    logger.debug('Salvando imagem no diretório especificado')
    try:
        output_file = os.path.join(output_path, img_name)
        fig.savefig(output_file, dpi=300)
        logger.info(f'Imagem salva com sucesso em {output_file}')
    except Exception as e:
        logger.error(f'Erro ao salvar imagem. Exception lançada: {e}')

# Função auxiliar de plotagem gráfica
def plot_file_param(df, col, ax, top_n=20, palette='Blues_r'):
    """
    Função auxiliar para plotagem de gráfico de barras utilizando parâmetro de arquivo
    
    Parâmetros
    ----------
    :param df: base de dados gerada a partir do report de diretório [type: pd.DataFrame]
    :param col: variável da base a ser plotada [type: string]
    :param ax: eixo de plotagem [type: Axes]
    :param top_n: filtro de top n arquivos dado o parâmetro de ordenação [type: int, default=20]
    :param palette: paleta de cores da plotagem [type: string, default='viridis']
    """
    
    # Ordenando e plotando visão arquivo        
    df = df.sort_values(by=col, ascending=False)
    if top_n > 0:
        df = df.iloc[:top_n, :]
    sns.barplot(y='arquivo', x=col, data=df, ax=ax, palette=palette)
  
# Visão geral do diretório
def visao_geral_dir(df, **kwargs):
    """
    Função responsável por gerar uma plotagem de visão geral do diretório
    
    Parâmetros
    ----------
    :param df: base de dados com o report gerado [type: pd.DataFrame]
    :param kwrgs
    
    Retorno
    -------
    Essa função não retorna nenhum parâmetro além da plotagem gráfica
    """
    
    # Definição de eixos usando GridSpec
    fig = plt.figure(constrained_layout=True, figsize=(17, 6))
    gs = GridSpec(1, 3, figure=fig)

    # Definindo eixos
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1:])

    # Realizando cálculos dos parâmetros
    sum_space = convert_kb_into_str(df['tamanho_kb'].sum())
    avg_space = convert_kb_into_str(df['tamanho_kb'].mean())
    qtd_files = len(df)

    # Definindo parâmetros de texto
    sum_text = 'Espaço total utilizado\nno diretório'
    files_text = 'Arquivos\nencontrados'
    avg_text = 'Tamanho médio\ndos arquivos'

    ax1.text(.5, .60, sum_space, fontsize=32, ha='center', color='white', style='italic', weight='bold',
             bbox=dict(facecolor='navy', alpha=0.5, pad=10, boxstyle='round, pad=.7'))
    ax1.text(.5, .75, sum_text, fontsize=18, ha='center', color='black', style='italic')

    ax1.text(.25, .18, qtd_files, fontsize=26, ha='center', color='white', style='italic', weight='bold',
             bbox=dict(facecolor='navy', alpha=0.5, pad=10, boxstyle='round, pad=.7'))
    ax1.text(.25, .32, files_text, fontsize=14, ha='center', color='black', style='italic')

    ax1.text(.75, .18, avg_space, fontsize=26, ha='center', color='white', style='italic', weight='bold',
             bbox=dict(facecolor='navy', alpha=0.5, pad=10, boxstyle='round, pad=.7'))
    ax1.text(.75, .32, avg_text, fontsize=14, ha='center', color='black', style='italic')

    ax1.axis('off')

    # Plotando gráfico de barras por usuário
    sns.distplot(df['tamanho_kb'], ax=ax2, color='navy', hist=False, rug=True, kde_kws={'shade': True})
    ax2.axvline(color='white', linestyle='--')
    ax2.set_title(f'Distribuição de Densidade do Tamanho dos Arquivos no Diretório', size=14)
    ax2.set_ylabel('Densidade')
    ax2.set_xlabel('Tamanho dos Arquivos')
    format_spines(ax2)

    # Finalizando plotagem
    plt.tight_layout()
    
    # Salvando figura
    if 'save' in kwargs and bool(kwargs['save']):
        output_path = kwargs['output_path'] if 'output_path' in kwargs else os.path.join(os.getcwd(), 'output/imgs')
        output_filename = kwargs['output_filename'] if 'output_filename' in kwargs else 'visao_geral_diretorio.png'
        save_fig(fig, output_path=output_path, img_name=output_filename)    

# Visão geral do usuário
def visao_geral_usuario(df, **kwargs):
    """
    Função responsável por gerar uma plotagem de visão geral do diretório
    
    Parâmetros
    ----------
    :param df: base de dados com o report gerado [type: pd.DataFrame]
    :param kwrgs
    
    Retorno
    -------
    Essa função não retorna nenhum parâmetro além da plotagem gráfica
    """
    
    # Definição de eixos usando GridSpec
    fig = plt.figure(constrained_layout=True, figsize=(17, 6))
    gs = GridSpec(1, 3, figure=fig)

    # Definindo eixos
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1:])

    # Agregando dados por usuário
    user_group = df.groupby(by='usuario_owner', as_index=False).agg({'tamanho_kb': 'sum',
                                                                     'arquivo': 'count',
                                                                     'dias_desde_criacao': 'mean',                        
                                                                     'dias_desde_ult_acesso': 'mean'})
    user_group.columns = ['usuario_owner', 'sum_tamanho_kb', 'qtd_arquivos', 'avg_dias_desde_criacao',
                          'avg_dias_desde_ult_acesso']

    # Espaço total alocado por usuário
    sns.barplot(x='usuario_owner', y='sum_tamanho_kb', data=user_group, palette='magma', ax=ax1)

    # Rótulos para o gráfico de barras
    total = user_group['sum_tamanho_kb'].sum()
    for p in ax1.patches:
        x = p.get_bbox().get_points()[:, 0]
        y = p.get_bbox().get_points()[1, 1]
        try:
            ax1.annotate(f'{convert_kb_into_str(y)}\n{100*(y/total):.1f}%', (x.mean(), y), 
                        ha='center', va='bottom', size=10)
        except ValueError as ve: # Erro por divisão por zero em entradas inexistentes pela quebra
            continue
    format_spines(ax1)
    ax1.set_xlabel('Usuário')
    ax1.set_ylabel('Soma de Espaço Alocado')
    ax1.set_title(f'Espaço Total Alocado por Usuário', size=14)
    ax1.set_ylim(0, user_group['sum_tamanho_kb'].max() + user_group['sum_tamanho_kb'].max() * .10)

    # Relação entre bases (tamanho versus dias desde último acesso)
    sns.scatterplot(x='tamanho_kb', y='dias_desde_ult_acesso', hue='usuario_owner', data=df, 
                    ax=ax2, size='tamanho_kb', palette='magma', sizes=(40, 400), alpha=.5)
    format_spines(ax2)
    ax2.set_xlabel('Espaço Total Alocado')
    ax2.set_ylabel('Dias Desde Último Acesso')
    ax2.set_title('Dispersão entre Tamanho das Bases e Dias sem Acesso', size=14)
    plt.tight_layout()
    
    # Salvando figura
    if 'save' in kwargs and bool(kwargs['save']):
        output_path = kwargs['output_path'] if 'output_path' in kwargs else os.path.join(os.getcwd(), 'output/imgs')
        output_filename = kwargs['output_filename'] if 'output_filename' in kwargs else 'visao_geral_usuarios.png'
        save_fig(fig, output_path=output_path, img_name=output_filename)  
  
# Visão geral de arquivos
def visao_geral_arquivos(df, figsize=(17, 17), top_n=20, palette='Blues_r',
                         plot_cols=['tamanho_kb', 'dias_desde_ult_acesso', 'filescope_score'], **kwargs):
    """
    Função para plotagem de visão geral relacionada aos arquivos
    
    Parâmetros
    :param df: base de dados gerada a partir do report de diretório [type: pd.DataFrame]
    :parma figsize: dimensões gráficas da plotagem [type: tuple, default=(17, 17)]
    :param top_n: filtro de top n arquivos dado o parâmetro de ordenação [type: int, default=20]
    :param palette: paleta de cores da plotagem [type: string, default='viridis']
    :param plot_cols: lista contendo três colunas alvo de análise [type: list]
        *default=['tamanho_kb', 'dias_desde_ult_acesso', 'filescope_score']
    """
    
    # Definição de eixos usando GridSpec
    fig = plt.figure(constrained_layout=True, figsize=figsize)
    gs = GridSpec(3, 1, figure=fig)

    # Definindo eixos
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])
    
    # Relizando plotagens
    for col, ax in zip(plot_cols, [ax1, ax2, ax3]):
        plot_file_param(df=df, col=col, ax=ax, top_n=top_n, palette=palette)
        format_spines(ax)
        ax.set_ylabel('Arquivo')
        
        # Rótulo para o gráfico gerado
        for p in ax.patches:
            x = p.get_bbox().get_points()[1, 0]
            y = p.get_bbox().get_points()[:, 1]
            try:
                if col == 'tamanho_kb':
                    ax.annotate(f'{convert_kb_into_str(x)}', (x, y.mean()), va='center', size=10)
                else:
                    ax.annotate(f'{int(x)}', (x, y.mean()), va='center', size=10)
            except ValueError as ve: # Erro por divisão por zero em entradas inexistentes pela quebra
                continue
        
    # Customizando plotagem 1
    ax1.set_title(f'Top {top_n} Arquivos de Maior Espaço Alocado (em KB)', size=14)
    ax1.set_xlabel('Tamanho do Arquivo (em KB)')
    
    # Customizando plotagem 2
    ax2.set_title(f'Top {top_n} Arquivos com Mais Tempo Sem Acesso', size=14)
    ax2.set_xlabel('Dias Desde o Último Acesso')
    
    # Customizando plotagem 3
    ax3.set_title(f'Top {top_n} com Maior Score filescope', size=14)
    ax3.set_xlabel('Score filescope (de 0 a 100)')
    
    plt.tight_layout()
    
    # Salvando figura
    if 'save' in kwargs and bool(kwargs['save']):
        output_path = kwargs['output_path'] if 'output_path' in kwargs else os.path.join(os.getcwd(), 'output/imgs')
        output_filename = kwargs['output_filename'] if 'output_filename' in kwargs else 'visao_geral_arquivos.png'
        save_fig(fig, output_path=output_path, img_name=output_filename)  

# Função geral para geração de report visual
def generate_visual_report(df, viz_dir=True, viz_user=True, viz_file=True, save=True,
                           output_path=os.path.join(os.getcwd(), 'output/imgs')):
    """
    Função responsável por gerenciar as plotagens gráficas no report visual

    Parâmetros
    ----------
    :param df: base de dados gerada a partir da função controle_de_diretorio() [type: pd.DataFrame]
    :param viz_dir: flag para plotagem de visao geral do diretorio [type: bool, default=True]
    :param viz_user: flag para plotagem de visao geral dos usuários [type: bool, default=True]
    :param viz_file: flag para plotagem de visao geral dos arquivos [type: bool, default=True]
    :param save: flag booleano para indicar o salvamento dos arquivos em disco [type: bool, default=True]
    :param output_path: diretório para salvamento dos arquivos [type: string, default=cwd() + 'output/imgs']  
    """

    # Gerando plotagens
    if viz_dir:
        visao_geral_dir(df=df, save=save, output_path=output_path)
    if viz_user:
        visao_geral_usuario(df=df, save=save, output_path=output_path)
    if viz_file:
        visao_geral_arquivos(df=df, save=save, output_path=output_path) 

