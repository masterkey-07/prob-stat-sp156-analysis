import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_donut_chart(df, title, min_percent=5):
    """
    Gera um gráfico de rosca agrupando categorias pequenas em 'Outros'.
    
    Parâmetros:
    - df: DataFrame contendo as colunas 'tema' e 'assunto'.
    - title: Título do gráfico.
    - min_percent: Percentual mínimo para que um item não seja agrupado em "Outros".
    """
    
    # Preparando os dados para o gráfico
    tema_assunto_count = df.groupby(['tema', 'assunto']).size().unstack(fill_value=0)

    # Função para agrupar os valores pequenos em "Outros"
    def group_small_categories(sizes, labels, min_percent):
        total = sum(sizes)
        grouped_sizes = []
        grouped_labels = []
        others = 0

        for i, size in enumerate(sizes):
            percent = (size / total) * 100
            if percent >= min_percent:
                grouped_sizes.append(size)
                grouped_labels.append(labels[i])
            else:
                others += size

        if others > 0:
            grouped_sizes.append(others)
            grouped_labels.append('Outros')

        return grouped_sizes, grouped_labels

    # Plotando gráfico de Rosquinha com agrupamento de "Outros"
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, tema in enumerate(tema_assunto_count.index):
        sizes = tema_assunto_count.loc[tema]
        labels = sizes.index
        
        # Agrupando categorias pequenas
        grouped_sizes, grouped_labels = group_small_categories(sizes, labels, min_percent)
        
        # Plotando o gráfico de rosca
        ax.pie(grouped_sizes, labels=grouped_labels, startangle=90, counterclock=False, 
               wedgeprops=dict(width=0.3, edgecolor='w'), 
               autopct='%1.1f%%', pctdistance=0.85)
        
        # Desenhando o círculo no centro para dar o efeito de rosca
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)
        plt.title(f'{title} - {tema}')
        plt.show()



def plot_bar_chart_by_year(df, title):
    # Convertendo a coluna de data para datetime
    df["data de abertura"] = pd.to_datetime(df["data de abertura"])

    # Extraindo o ano
    df['year'] = df["data de abertura"].dt.year

    # Contando o número de ocorrências de cada assunto dentro de cada tema por ano
    count_data = df.groupby(['year', "tema", "assunto"]).size().reset_index(name='count')

    # Plotando o gráfico de barras
    plt.figure(figsize=(12, 8))
    sns.barplot(data=count_data, x='year', y='count', hue="assunto", palette='muted')
    plt.title(title)
    plt.xlabel('Ano')
    plt.ylabel('Contagem')
    plt.legend(title='Assunto')
    plt.xticks(rotation=45)
    plt.show()

def plot_bar_chart_by_year_per_assunto(df, title):
    """
    Gera gráficos de barras separados para cada 'assunto', mostrando a distribuição por ano.
    
    Parâmetros:
    - df: DataFrame contendo as colunas de data, tema, e assunto.
    - title: Título base para os gráficos.
    """
    
    # Convertendo a coluna de data para datetime
    df["data de abertura"] = pd.to_datetime(df["data de abertura"])

    # Extraindo o ano
    df['year'] = df["data de abertura"].dt.year

    # Lista única de assuntos
    assuntos = df["assunto"].unique()

    # Gerando um gráfico de barras para cada assunto
    for assunto in assuntos:
        # Filtrando os dados para o assunto atual
        df_assunto = df[df["assunto"] == assunto]

        # Contando o número de ocorrências por tema e ano
        count_data = df_assunto.groupby(['year', "tema"]).size().reset_index(name='count')

        # Plotando o gráfico de barras
        plt.figure(figsize=(12, 8))
        sns.barplot(data=count_data, x='year', y='count', hue="tema", palette='muted')
        plt.title(f'{title} - Assunto: {assunto}')
        plt.xlabel('Ano')
        plt.ylabel('Contagem')
        plt.legend(title='Tema')
        plt.xticks(rotation=45)
        plt.show()