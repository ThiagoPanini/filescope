<h1 align="center">
  <a href="https://pypi.org/project/filescope/"><img src="https://i.imgur.com/qgT6wPW.png" alt="filescope logo"></a>
</h1>

<div align="center">
  <strong>:open_file_folder: Managing files and local disk usage in an Operational System :open_file_folder:</strong>
</div>
<br/>

<div align="center">  
  
  ![Release](https://img.shields.io/badge/release-ok-brightgreen)
  [![PyPI](https://img.shields.io/pypi/v/xplotter?color=blueviolet)](https://pypi.org/project/filescope/)
  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/filescope?color=green)
  ![PyPI - Status](https://img.shields.io/pypi/status/filescope)

</div>

<div align="center">  
  
  ![Downloads](https://img.shields.io/pypi/dm/filescope?color=darkblue)
  ![Downloads](https://img.shields.io/pypi/dw/filescope?color=blue)
  ![Downloads](https://img.shields.io/pypi/dd/filescope?color=lightblue)

</div>

<br/>


## Table of content

- [About filescope](#about-filescope)
  - [Package structure](#package-structure)
- [Features](#features)
  - [Filescope Score](#filescope-score)
- [Installing the package](#installing-the-package)
- [Examples](#examples)
  - [Manager module](#manager-module)
- [Contribution](#contribution)
- [Social Media](#social-media)

___

## About filescope

Have you ever questioned yourself about how good it could be to have some kind of engine that helps user to manage files and disk usage in a shared directory of a company? Maybe it's the case that you work in a team and you all use the same directory to share files and projects but, as times passes by, you all start to face problems on disk space available or the storage of huge files made from people that are not on the team anymore. How can you handle it without searching files one by one in a directory with thousands of them?

Here is the answear: the `filescope` python package. The example above is just one of the most motivational for building this tool, but I want you to look at this package and see an instrument that makes the management of files in an operational system easier, whether you are in a company or in our personal environment. The big idea behind this new implementation is to improve analytics on local directories for helping users to make good decisions about which files are no longer being used and that are taking up a large amount of disk space.

At the end of the day, the `filescope` python package provides a *Filescope Score* that are computed using some attributes of files in a disk and can be used for guidance on file mangement decisions. The score will be detailed along this documentation.

___

### Package structure

By now, the `filescope` package has one module called `manager` that includes all the functions for applying analytics on local folders or even making some basic actions like copying files from a source to a destiny. There is also good effort being made for adding up visual analysis using fetures extracted from local folders.

| Module      | Description                                                                 | Functions/Methods  | Lines of Code (approx) |
| :---------: | :-------------------------------------------------------------------------: | :----------------: | :--------------------: |
| `manager`   | Functions for managing files and extracting features from local directories |         15         |         ~850           |

It is also good to say that the filescope package uses the `logging` package for log the actions inside funtions calls. The logger configuration is built inside the manager module and can be acessible and changed by modifying the python file associated.

___

## Features

After a general overview of the package, it's time to go a little deeper on its functionalities. So, this section will allocate some of the main package features divided into two groups: file handling and directory management.

### File Handling

One of the greatest features of filescope is to provide users the hability to use built in functions to 

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
