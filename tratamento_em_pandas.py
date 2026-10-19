import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import urllib.request
import json

# Carregar o dataset
df = pd.read_csv('vendas_completas.csv')
# Converter DataVenda para formatos de datas para análise de serie temporal
df['DataVenda'] = pd.to_datetime(df['DataVenda'])

# 1. Vendas por mês
df['AnoMes'] = df['DataVenda'].dt.to_period('M').astype(str)
vendas_tempo = df.groupby('AnoMes')['ValorVenda'].sum().reset_index()

# Criar gráfico de linha interativo
fig_tempo = px.line(
    vendas_tempo, 
    x='AnoMes', 
    y='ValorVenda',
    markers=True,
    title='Evolução de vendas por mês',
)

#Colocar cores roxo e lanraja
fig_tempo.update_traces(
    line=dict(color='purple', width=3),
    marker=dict(size=10, color='orange', line=dict(width=1, color='white'))
)

# Remover rótulos de X e Y
fig_tempo.update_layout(
    title='Evolução de vendas por mês',
    xaxis=dict(
        title=None,
    ),
    yaxis=dict(
        title=None,
    ),
    template='plotly_white',
    margin=dict(l=20, r=20, t=20, b=20) # 
)
fig_tempo.update_traces(line=dict(width=3), marker=dict(size=8))
fig_tempo.show()


# 2. Top Produtos por Vendas
produtos_mais_vendidos = df.groupby('Produto')['QuantidadeVendida'].sum().reset_index().sort_values(by='QuantidadeVendida', ascending=False)

# Agrupar dados por vendas totais/brutas
produtos_por_receita = df.groupby('Produto')['ValorVenda'].sum().reset_index().sort_values(by='ValorVenda', ascending=True)

# Criar gráfico de barra horizontal para vendas
fig_receita = px.bar(
    produtos_por_receita, 
    x='ValorVenda', 
    y='Produto',
    orientation='h',
    title='Top Produtos por Vendas (R$)',
    labels={'ValorVenda': 'Renda bruta(R$)', 'Produto': 'Produtos'},
    text='ValorVenda',
    color='ValorVenda',
    color_continuous_scale='Purples'
)

# Formatação de moeda e layout
fig_receita.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
fig_receita.update_layout(
    xaxis_title='Total Revenue ($)', 
    yaxis_title='Product', 
    template='plotly_white',
    xaxis_tickprefix='$'
)
fig_receita.show()

# 3. Vendas por Estado
# Agrupar por estado
vendas_por_estado = df.groupby('Estado')['ValorVenda'].sum().reset_index()
vendas_por_estado = vendas_por_estado.sort_values(by='ValorVenda', ascending=False)

# Criar gráfico de barras com Plotly Express
fig_estado = px.bar(
    vendas_por_estado, 
    x='Estado', 
    y='ValorVenda',
    text='ValorVenda',
    title='Vendas por Estado',
    labels={'ValorVenda': '', 'Estado': ''},
    color_discrete_sequence=['#54278f']
)

# Formatação de rótulos e layout
fig_estado.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
fig_estado.update_layout(template='plotly_white')
fig_estado.show()

# 4. Mapa do Brasil/ Heatmap
vendas_por_estado = df.groupby('Estado')['ValorVenda'].sum().reset_index()

# Acrescentado estados
#  Lista completa de todos os estados do Brasil para incluir os que faltam com valor 0
todos_estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 
                 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
df_todos = pd.DataFrame({'Estado': todos_estados})

# Mesclar com os dados reais, substituindo ausentes por 0
df_mapa = pd.merge(df_todos, vendas_por_estado, on='Estado', how='left').fillna(0)

url_geojson = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
with urllib.request.urlopen(url_geojson) as response:
    brazil_geojson = json.loads(response.read().decode('utf-8'))

# Criar o mapa coroplético interativo
fig = px.choropleth(
    df_mapa,
    geojson=brazil_geojson,
    locations='Estado',                # Coluna do seu dataframe com as siglas (SP, RJ, etc.)
    featureidkey='properties.sigla',   # Chave correspondente no GeoJSON
    color='ValorVenda',                # Coluna que define a intensidade da cor
    #color_continuous_scale='Purples',  # Escala em tons de roxo (SP será o mais escuro)
    color_continuous_scale=[
        [0.0, '#ffffff'],
        [0.0, '#dadaeb'],  # Lilás/roxo clarinho visível para os menores valores
        [0.5, '#807dba'],  # Roxo médio
        [1.0, '#3f007d']   # Roxo escuro profundo para São Paulo
    ],
    range_color=[df_mapa['ValorVenda'].min() + 1, df_mapa['ValorVenda'].max()], # Ignora o zero na escala de cores
    title='Total de Vendas por Estado do Brasil',
    labels={'ValorVenda': 'Total de Vendas ($)'}
)

# Ajustar o foco e o layout do mapa para o Brasil
fig.update_geos(
    fitbounds="locations", 
    visible=False)
fig.update_layout(
    margin={"r":0,"t":40,"l":0,"b":0},
    template='plotly_white')
fig.show()
