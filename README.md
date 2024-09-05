# Análise de Problemas de Moradia e SP156

Este projeto tem como objetivo analisar os dados relacionados a problemas de moradia e demandas pelo sistema SP156, utilizando Python e Jupyter Notebooks para preparação e exploração de dados. O projeto é dividido em três notebooks principais:

## Arquivos

- `prepare_dataset.ipynb`: Este notebook é responsável por baixar e preparar os dados que serão usados nas análises. Ele realiza a limpeza e o pré-processamento das informações necessárias para garantir que os dados estejam prontos para uso.

- `homeless_problem_analysis.ipynb`: Este notebook contém a análise dos problemas relacionados à moradia. Ele faz uso dos dados previamente preparados para gerar insights e visualizações sobre a situação das pessoas em situação de rua.

- `sp156_analysis.ipynb`: Focado na análise de dados do sistema SP156, este notebook apresenta um estudo das demandas e reclamações registradas ao longo do tempo, oferecendo gráficos e estatísticas relevantes para entender o comportamento da população em relação aos serviços públicos.

## Como preparar o projeto

### 1. Clonar o repositório

Primeiro, clone o repositório do projeto em sua máquina:

```bash
git clone https://github.com/seuusuario/seuprojeto.git
cd seuprojeto
```

### 2. Instalar as dependências

O projeto utiliza as bibliotecas listadas no arquivo `requirements.txt`. Para instalar todas as dependências necessárias, execute:

```bash
pip install -r requirements.txt
```

### 3. Preparar o conjunto de dados

Após instalar as dependências, execute o notebook `prepare_dataset.ipynb` para baixar e preparar os dados:

1. Abra o Jupyter Notebook:

```bash
jupyter notebook
```

2. No navegador, abra o arquivo `prepare_dataset.ipynb`.

3. Execute todas as células para baixar e processar os dados.

### 4. Executar as análises

Depois de preparar os dados, você pode executar os notebooks de análise:

- **Para analisar problemas de moradia**, abra e execute o `homeless_problem_analysis.ipynb`.
- **Para analisar os dados do SP156**, abra e execute o `sp156_analysis.ipynb`.

Ambos os notebooks geram gráficos e estatísticas com base nos dados processados.
