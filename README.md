<h1 align="center">
  <a href="https://pypi.org/project/filescope/"><img src="https://i.imgur.com/qgT6wPW.png" alt="filescope logo"></a>
</h1>

<div align="center">
  <strong>:open_file_folder: Gerenciamento de arquivos em diretórios locais :open_file_folder:</strong>
</div>
<br/>

<div align="center">  
  
  ![Release](https://img.shields.io/badge/release-ok-brightgreen)
  [![PyPI](https://img.shields.io/pypi/v/filescope?color=blueviolet)](https://pypi.org/project/filescope/)
  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/filescope?color=green)
  ![PyPI - Status](https://img.shields.io/pypi/status/filescope)

</div>
<br/>

Biblioteca Python criada para facilitar o gerenciamento e a análise de arquivos armazenados em diretórios locais do sistema operacional. Com o pacote `filescope`, é possível validar a presença de arquivos em diretórios específicos, realizar cópias entre arquivos de diferentes diretórios ou até mesmo gerar um report analítico e visual completo contendo informações relevantes a respeito dos arquivos presentes em um diretório específico, como tamanho, dias desde a criação, dias sem utilização, modificação ou acesso e um score específico (denominado *filescope_score*) que penaliza arquivos de alto tamanho e que estão há muito tempo sem acesso.

## Table of content

- [Features](#features)
    - [Manuseio de arquivos](#manuseio-de-arquivos)
    - [Gerenciamento de Diretórios](#gerenciamento-de-diretórios)
- [Instalação](#instalação)
- [Utilização](#utilização)

___

## Features

Em sua versão atual, o pacote `filescope` conta com o módulo `manager`, sendo este responsável por alocar as principais funcionalidades relacionadas ao gerenciamento e a análise de arquivos em diretórios. Entre o detalhamento aqui proposto, as ferramentas deste pacote serão divididas em dois principais grupos: manuseio de arquivos e gerenciamento de diretórios.

### Manuseio de Arquivos

Uma das grandes vantagens do pacote filescope é a de proporcionar aos usuários blocos de código previamente gerenciados para algumas operações envolvendo arquivos, como a validação e a cópia. A função `valida_arquivo_origem()`, por exemplo, é capaz de retornar uma resposta booleana relacionada a presença de um determinado arquivo em um determinado diretório. Já a função `valida_dt_mod_arquivo()`, por sua vez, além de validar a presença de um arquivo em um diretório, também analisa se o dado arquivo está devidamente atualizado seguindo critérios fornecidos pelo usuário, permitindo assim, verificar se dado arquivo neste diretório alvo foi modificado pela última vez no mês atual. Ainda neste bloco, a função `copia_arquivo()`, realiza a cópia de arquivos baseada em uma origem e um destino fornecidos pelo usuário.

Em `examples/valida_e_copia_arquivo.py`, será possível encontrar um exemplo detalhado de utilização deste grupo de funcionalidades do pacote filescope.

### Gerenciamento de Diretórios

Talvez a funcionalidade mais impactante deste pacote tenha raízes no gerenciamento de arquivos em um diretório específico. Considerando uma utilização corporativa como motivação, a função `controle_de_diretorio()` recebe simplesmente um parâmetro de diretório alvo como argumento para realizar uma varredura completa em todos os arquivos presentes neste caminho, extraindo informações extremamente relevantes a serem analisadas posteriormente pelos usuários como insumo básico para tomada de decisões. O resultado da execução desta função é um report gerencial representando uma linha por arquivo e contendo as seguintes informações:

* **_diretorio:_** informação do diretório (incluindo subpastas) do referido arquivo;
* **_arquivo:_** nome do arquivo analisado pela função;
* **_tamanho_kb:_** tamanho total do arquivo em KB;
* **_usuario_owner:_** usuário owner vinculado ao arquivo;
* **_dt_criacao:_** data de criação do referido arquivo;
* **_dias_desde_criacao:_** quantidade de dias contados a partir da criação do arquivo até a data de execução do report;
* **_dt_ult_mod:_** data de última modificação do referido arquivo;
* **_dias_desde_ult_mod:_** quantidade de dias contados a partir da última modificação do arquivo até a data de execução do report;
* **_dt_ult_acesso:_** data de último acesso do referido arquivo;
* **_dias_desde_ult_acesso:_** quantidade de dias contados a partir do último acesso do arquivo até a data de execução do report;
* **_filescope_score:_** score `filescope` calculado a partir de fórmula que penaliza arquivos pesados e sem acesso (a ser detalhada);
* **_dt_relatorio:_** data de execução e extração do relatório.

Como visto na lista acima, além de retornar informações extremamente relevantes para o controle de um diretório, a função é capaz de realizar um cálculo próprio consolidado na variável `filescope_score`, sendo esta definida por:

<div align="center">
  <img src="https://render.githubusercontent.com/render/math?math=\text{filescope}_\text{score}=2\text{tkb} \times \text{ddc} \times 2\text{dda} \times \text{ddm}">
</div>

Onde:
* tkb = tamanho_kb
* ddc = dias_desde_criacao
* dda = dias_desde_ult_acesso
* ddm = dias_desde_ult_mod

## Instalação

A última versão do pacote `filescope` encontra-se publicada no repositório <a href="https://pypi.org/project/filescope/">PyPI</a>.

> :pushpin: **Nota:** como boa prática de utilização em qualquer projeto Python, a construção de um <a href="https://realpython.com/python-virtual-environments-a-primer/">ambiente virtual</a> se faz necessária para um maior controle das funcionalidades e das dependências atreladas ao código. Para tal, o bloco abaixo considera os códigos necessários a serem executados no cmd para a criação de ambientes virtuais Python nos sistemas Linux e Windows.
> 

```bash
# Criação e ativação de venv no linux
$ python -m venv <path_venv>/<nome_venv>
$ source <path_venv>/<nome_venv>/bin/activate

# Criação e ativação de venv no windows
$ python -m venv <path_venv>/<nome_venv>
$ <path_venv>/<nome_venv>/Scripts/activate
```

Com o ambiente virtual ativo, basta realizar a atualização do `pip` (opcional) seguida da instalação do pacote:

```bash
$ pip install --upgrade pip
$ pip install filescope
```

A construção do pacote `filescope` é feita utilizando, como pilar, bibliotecas de modelagem fundamental em Python. Dessa forma, ao realizar a instação no ambiente virtual, é esperado que outras bibliteocas dependentes também sejam instaladas. O output esperado no prompt de comando após a instalação deve ser semelhante ao ilustrado abaixo:

```
Collecting filescope
  Downloading filescope-0.0.3-py3-none-any.whl (2.6 kB)
Collecting pandas==1.1.5
  Downloading pandas-1.1.5-cp38-cp38-manylinux1_x86_64.whl (9.3 MB)
     |████████████████████████████████| 9.3 MB 8.1 MB/s 
Collecting filescope
  Downloading filescope-0.0.2-py3-none-any.whl (2.5 kB)
Collecting numpy>=1.15.4
  Downloading numpy-1.20.2-cp38-cp38-manylinux2010_x86_64.whl (15.4 MB)
     |████████████████████████████████| 15.4 MB 9.6 MB/s 
Collecting pytz>=2017.2
  Downloading pytz-2021.1-py2.py3-none-any.whl (510 kB)
     |████████████████████████████████| 510 kB 10.3 MB/s 
Collecting python-dateutil>=2.7.3
  Downloading python_dateutil-2.8.1-py2.py3-none-any.whl (227 kB)
     |████████████████████████████████| 227 kB 10.4 MB/s 
Collecting six>=1.5
  Downloading six-1.15.0-py2.py3-none-any.whl (10 kB)
Installing collected packages: six, pytz, python-dateutil, numpy, pandas, filescope
Successfully installed filescope-0.0.2 numpy-1.20.2 pandas-1.1.5 python-dateutil-2.8.1 pytz-2021.1 six-1.15.0
```

## Utilização

A partir desse ponto, a biblioteca `filescope` pode ser importada em scripts Phyton. Exemplos práticos podem ser encontrados neste repositório no diretório `examples/`. Ilustrando uma aplicação relacionada a criação de um report gerencial e visual de um diretório, o código abaixo ilustra a utilização de algumas funções do pacote que encapsulam tais ações:

```python
# Importando bibliotecas
from filescope.manager imoport controle_de_diretorio, generate_visual_report

# Extraindo report analítico de arquivos
df_root = controle_de_diretorio(root=SRC_PATH, output_filepath=ROOT_FILE)

# Gerando e salvando report visual
generate_visual_report(df=df_root, output_path=OUTPUT_PATH)
```

Ao executar o código acima com as devidas configurações de caminhos especificadas pelas variáveis de caminhos passadas como argumentos, espera-se obter um resultado em uma pasta de saída contendo um arquivo csv analítico com informações dos arquivos em um diretório, além de imagens com explorações e insights visuais sobre o consumo deste diretório.

```
examples/output
├── root_control.csv
├── visao_geral_arquivos.png
├── visao_geral_diretorio.png
└── visao_geral_usuarios.png
```

A função `generate_visual_report()` é extremamente valiosa para a coleta de insights visuais sobre o conteúdo do diretório analisado. Como exemplo, a imagem abaixo ilustra o conteúdo presente, por padrão, em `visao_geral_diretorio.png`:

<div allign="center">
  <img src="https://i.imgur.com/dHy8Exx.png">
</div>
