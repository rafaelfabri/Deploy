#importando as bibliotecas
import pandas as pd
import numpy as np
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from pyproj import Proj
from dash.dependencies import Input, Output
import dash
import plotly.graph_objects as go


#importando base de dados já concatenada
df = pd.read_csv('base_03.csv', sep=',')
print(df.head())

#token para o mapa de notificações
my_token = 'pk.eyJ1IjoicmFmYWVsZmFicmkiLCJhIjoiY2trcmo3Zzk5MDd1MDJ2b2l1eXZ5MHZrNyJ9.ND1Yp9n8IMa37hkOno9HoA'


#converção dos dados de UTM para Lat, Lon
myproj = Proj(proj='utm', zone=22, ellps='WGS84', south=True)
lon, lat = myproj(longitude=df['NOX'], latitude=df['NOY'], inverse=True)
df['lat'] = lat
df['lon'] = lon


'''
#criando coluna localidade 
df['localidade'] = "l"

#criando coluna UTD
df['UTD'] = 'l'

#atribuir nome da localidade atraves do numero 
for i in df['LOCAL'].index:

    if(df['LOCAL'][i] == 233):
        df['localidade'][i] = 'Capao Bonito'
    elif(df['LOCAL'][i] == 218):
        df['localidade'][i] = 'Barra do Turvo'
    elif(df['LOCAL'][i]==235):
        df['localidade'][i] = 'Angatuba'
    elif(df['LOCAL'][i] == 241):
        df['localidade'][i] = 'Itaporanga'
    elif(df['LOCAL'][i] == 232):
        df['localidade'][i] = 'Ribeirao Grande'
    elif(df['LOCAL'][i] == 224):
        df['localidade'][i] = 'Ribeirao Branco'
    elif(df['LOCAL'][i] == 237):
        df['localidade'][i] = 'Itarare'
    elif(df['LOCAL'][i] == 239):
        df['localidade'][i] = 'Itabera'
    elif(df['LOCAL'][i] == 240):
        df['localidade'][i] = 'Riversul'
    elif(df['LOCAL'][i] == 236):
        df['localidade'][i] = 'Itapeva'
    elif(df['LOCAL'][i] == 234):
        df['localidade'][i] = 'Buri'
    elif(df['LOCAL'][i] == 222):
        df['localidade'][i] = 'Guapiara'
    elif(df['LOCAL'][i] == 220):
        df['localidade'][i] = 'Apiai'
    elif(df['LOCAL'][i] == 231):
        df['localidade'][i] = 'Campina do Monde Alegre'
    elif(df['LOCAL'][i] == 223):
        df['localidade'][i] = 'Barra do Chapeu'
    elif(df['LOCAL'][i] == 244):
        df['localidade'][i] = 'Fartura'
    elif(df['LOCAL'][i] == 238):
        df['localidade'][i] = 'Bom Sucesso de Itarare'
    elif(df['LOCAL'][i] == 245):
        df['localidade'][i] = 'Nova Campina'
    elif(df['LOCAL'][i] == 246):
        df['localidade'][i] = 'Taquarivai'
    elif(df['LOCAL'][i] == 242):
        df['localidade'][i] = 'Barra Antonina'
    if(df['LOCAL'][i] == 245):
        df['localidade'][i] = 'Nova Campina'
    elif(df['LOCAL'][i] == 243):
        df['localidade'][i] = 'Coronel Macedo'
    elif(df['LOCAL'][i] == 221):
        df['localidade'][i] = 'Itarirapua Paulista'
    elif(df['LOCAL'][i] == 217):
        df['localidade'][i] = 'Iporanga'
    elif(df['LOCAL'][i] == 219):
        df['localidade'][i] = 'Ribeira'


#Atraves do nome da localidade atribuir a UTD
for i in df['LOCAL'].index:

    if(df['localidade'][i] == 'Apiai' or df['localidade'][i] == 'Iporanga' or
       df['localidade'][i] == 'Barra Antonina' or df['localidade'][i] == 'Ribeira' or
       df['localidade'][i] == 'Barra do Turvo'):

        df['UTD'][i] = 'Apiai'

    if(df['localidade'][i] == 'Capao Bonito' or df['localidade'][i] == 'Angatuba' or df['localidade'][i] == 'Buri' or
       df['localidade'][i] == 'Guapiara'):

        df['UTD'][i] = 'Capao Bonito'

    if(df['localidade'][i] == 'Itapeva' or df['localidade'][i] == 'Nova Campina' or
       df['localidade'][i] == 'Taquarivai' or df['localidade'][i] == 'Itabera' or
       df['localidade'][i] == 'Ribeirao Branco'):

        df['UTD'][i] = 'Itapeva'

    if(df['localidade'][i] == 'Itaporanga' or df['localidade'][i] == 'Bom Sucesso de Itarare' or
       df['localidade'][i] == 'Itarare' or df['localidade'][i] == 'Fartura'):

        df['UTD'][i] = 'Itaporanga'
'''


#CRIANDO UM NOVO DATAFRAME - para fazer o gráfico de barras

#criando variáveis do tipo lista para atribuição de valores
utd = []
status = []
quantidade = []


#condição de repetição para atribuir valores de quantidade por UTD e STATUS na ordem para cada variável
for i in range(0, len(df.groupby('UTD')['STATUS'].value_counts()), 1):

    #atribuindo valores
    utd.append( df.groupby('UTD')['STATUS'].value_counts().keys()[i][0] )
    status.append( df.groupby('UTD')['STATUS'].value_counts().keys()[i][1] )
    quantidade.append( df.groupby('UTD')['STATUS'].value_counts().values[i] )

#criando o novo DataFrame apartir das variáveis
df_quant = pd.DataFrame(columns=['UTD', 'STATUS', 'QUANTIDADE'])
df_quant['UTD'] = utd
df_quant['STATUS'] = status
df_quant['QUANTIDADE'] = quantidade

#criando um DataFrame para gráfico de colunas do setor
status_setor = []
setor = []
quant_setor = []

for i in range(0, len(df.groupby('STATUS')['Setor'].value_counts()), 1):
  status_setor.append(df.groupby('STATUS')['Setor'].value_counts().keys()[i][0])
  setor.append(df.groupby('STATUS')['Setor'].value_counts().keys()[i][1])
  quant_setor.append(df.groupby('STATUS')['Setor'].value_counts().values[i])

df_quant_setor = pd.DataFrame(columns=['SETOR', 'STATUS', 'QUANTIDADE'])

df_quant_setor['SETOR'] = setor
df_quant_setor['STATUS'] = status_setor
df_quant_setor['QUANTIDADE'] = quant_setor


#CRIANDO COLUNA COLOR - para atribuir as cores em hexadecimal para o DataFrame df
df['color'] = 'l'

#condição de repetição para atribuir valor linha por linha
for i in df['Local'].index:

    # condiççoes para atribuir dados em cada linha
    if(df['STATUS'][i] == 'Notificacao_90'):
        df['color'][i] =  '#FFFF00'
    if(df['STATUS'][i] == 'Executado'):
        df['color'][i] = '#00FF00'
    if(df['STATUS'][i] == 'Notificado'):
        df['color'][i] = '#0000FF'
    if (df['STATUS'][i] == 'Notificacao_180'):
        df['color'][i] = '#FF0000'


#CRIANDO COLUNA COLOR - para atribuir as cores em hexadecimal para o DataFrame df_quant
df_quant['COLOR'] = 'l'

#condição de repetição para atribuir valor linha por linha
for i in df_quant['UTD'].index:

    # condiççoes para atribuir dados em cada linha
    if(df_quant['STATUS'][i] == 'Notificacao_90'):
        df_quant['COLOR'][i] =  '#FFFF00'
    if(df_quant['STATUS'][i] == 'Executado'):
        df_quant['COLOR'][i] = '#00FF00'
    if(df_quant['STATUS'][i] == 'Notificado'):
        df_quant['COLOR'][i] = '#0000FF'
    if(df_quant['STATUS'][i] == 'Notificacao_180'):
        df_quant['COLOR'][i] =  '#FF0000'

#CRIANDO COLUNA COLOR - para atribuir as cores em hexadecimal para o DataFrame df_quant
df_quant_setor['COLOR'] = 'l'

#condição de repetição para atribuir valor linha por linha
for i in df_quant_setor['SETOR'].index:

    # condições para atribuir dados em cada linha
    if(df_quant_setor['STATUS'][i] == 'Notificacao_90'):
        df_quant_setor['COLOR'][i] =  '#FFFF00'
    if(df_quant_setor['STATUS'][i] == 'Executado'):
        df_quant_setor['COLOR'][i] = '#00FF00'
    if(df_quant_setor['STATUS'][i] == 'Notificado'):
        df_quant_setor['COLOR'][i] = '#0000FF'
    if(df_quant_setor['STATUS'][i] == 'Notificacao_180'):
        df_quant_setor['COLOR'][i] =  '#FF0000'


#CRIANDO COLUNA text - para atribuir a legenda de cada ponto de localização
df['text'] = 'l'

#condição de repetição para atribuir o texto
for i in df['Local'].index:
    df['text'][i] = df['NOME'][i] + '<br>' + 'UC: ' + str(df['UC'][i])  + '<br>' + 'Dta inc: ' + str(df['Data_inicio'][i]) + '<br>' + 'Dta concl: ' + str(df['Data_conclusao'][i])


print(df.dtypes)
#COMEÇANDO A REALIZAR O MAPA DE NOTIFICAÇÕES E A ETAPA DE DASHBOARD

#instanciando Dash app - DASHBOOTSTRAP
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.SOLAR])

#criação do layout
app.layout = html.Div([

    #primeira linha
    dbc.Row([

        #primeira coluna
        dbc.Col(dbc.Card([
                dbc.CardImg(src='/assets/neoenergia.jpg')
                ]), #width={'size':1,'offset':0, 'order':1},
                    xs=1, sm=1, md=1, lg=1, xl=1,
        ),

        #segunda coluna
        dbc.Col(dbc.Card([
                dbc.CardImg(src='/assets/ELEKTRO1.jpg')
                ]), #width={'size':1, 'offset':0, 'order':2},
                    xs=1, sm=1, md=1, lg=1, xl=1,
        ),

        #terceira coluna
        dbc.Col(html.H1('Mapa de Notificações SDP', className='font-weight-bold text-success'),
                    #width={'size':8,'offset':1,'order':3}
                    xs=8, sm=8, md=8, lg=8, xl=8,
        )

    ]),

    #segunda linha
    dbc.Row([

        #primeira coluna
        dbc.Col(dcc.Input(id = 'num_uc', placeholder='Número UC...', type='number'),
                    width = {'size':1, 'offset':1},
                    #xs=2, sm=2, md=2, lg=2, xl=2,
        ),

        #segunda coluna
        dbc.Col(dcc.Dropdown(id = 'botoes_mapa', value=['Itapeva'], multi = True,
                             options=[{'label' : i,'value' : i} for i in df['UTD'].unique()]),
                    width = {'size':8,'offset':1}
        )

    ]),

    #terceira linha
    dbc.Row(

        #primeira coluna
        dbc.Col(dcc.Graph(id = 'mapa', figure = {}), #width={'size':12, 'offset':0,}
                    xs=12, sm=12, md=12, lg=12, xl=12)

    ),

    #quarta coluna
    dbc.Row([

        #primeira linha
        dbc.Col(dbc.Card([

                    dbc.CardHeader(html.H3('UTDs', className='font-weight-bold text-dark font-italic')),

                    dbc.CardBody([

                        html.H6('Escolha as UTDs', className='text-dark'),

                        dcc.Dropdown(id = "botoes_utd",
                                     options=[{'label' : i, 'value' : i} for i in sorted(df_quant['UTD'].unique())],
                                     value=['Itapeva'], className='text-dark', multi=True)

                    ]),

                ], color='info'
                ), width = {'size':3, 'offset':1}

        ),

        dbc.Col(dbc.Card([

                    dbc.CardHeader(html.H3('Gerência', className='font-weight-bold text-dark font-italic')),

                    dbc.CardBody([

                        dcc.Dropdown(id = 'botoes_setor',
                                     options=[{'label':i,'value':i} for i in sorted(df_quant_setor['SETOR'].unique())],
                                     value=['Gerencia Sudoeste Paulista'], multi=True)

                    ])

                ], color='info'
                ), width={'size':3, 'offset':3}

        )

    ]),


    dbc.Row([

        dbc.Col(dcc.Graph(id = 'barras', figure = {}), #width = {'size':6, 'offset':0, 'order':0}
                xs=6, sm=6, md=6, lg=6, xl=6),
        dbc.Col(dcc.Graph(id = 'setor', figure = {}), #width = {'size' : 6, 'offset':0, 'order':1}
                xs=6, sm=6, md=6, lg=6, xl=6)

    ]),


])

#callback
@app.callback(Output(component_id='mapa', component_property='figure'),
              Input(component_id='botoes_mapa', component_property='value'),
              Input(component_id='num_uc', component_property='value'))

#FUNÇÃO PARA ATRIBUIÇÃO DE VALORES E GERAÇÃO DOS GRÁFICOS
def update_graph(botoes_mapa, num_uc):

    #condições de filtro
    if(num_uc is None):
        dff = df.copy()
        dff = dff[dff['UTD'].isin(botoes_mapa)]
    else:
        dff = df.copy()
        dff = dff[dff['UTD'].isin(botoes_mapa)]
        dff = dff[dff['UC']==num_uc]

    #instanciando variável
    fig = go.Figure()

    #criando novos dataframe de acordo com cada tipo de status
    exece = dff[dff['STATUS'] == 'Executado']
    noti = dff[dff['STATUS'] == 'Notificado']
    noti_90 = dff[dff['STATUS'] == 'Notificacao_90']
    noti_180 = dff[dff['STATUS'] == 'Notificacao_180']

    #adicionando plots na figure
    fig.add_trace(go.Scattermapbox(lat=exece['lat'], lon=exece['lon'], text=exece['text'],
                                   marker=go.scattermapbox.Marker(color=exece['color']),
                                   name='Executado')
    )

    fig.add_trace(go.Scattermapbox(lat=noti['lat'], lon=noti['lon'], text=noti['text'],
                                   marker=go.scattermapbox.Marker(color=noti['color']),
                                   name='Notificado')
    )

    fig.add_trace(go.Scattermapbox(lat=noti_90['lat'], lon=noti_90['lon'], text=noti_90['text'],
                                   marker=go.scattermapbox.Marker(color=noti_90['color']),
                                   name='Notificado_90')
    )

    fig.add_trace(go.Scattermapbox(lat=noti_180['lat'], lon=noti_180['lon'], text=noti_180['text'],
                                   marker=go.scattermapbox.Marker(color=noti_180['color']),
                                   name='Notificado_180')
    )

    fig.update_layout(height=600)

    #definindo algumas configurações do layout
    fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=-23.9308137, lon=-49.2164035), zoom=8))
    fig.update_layout(mapbox_style="open-street-map"),

    #retornando fig
    return fig

#fazenco callback para o gráfico de barras
@app.callback(Output(component_id='barras', component_property='figure'),
              Input(component_id='botoes_utd', component_property='value'))

def update_graph_1(a):

    df_quant_copy = df_quant.copy()
    df_quant_copy = df_quant_copy[df_quant_copy['UTD'].isin(a)]

    #plot
    fig_bar = px.bar(df_quant_copy, x = 'UTD', y = 'QUANTIDADE', color = 'STATUS',
                     color_discrete_sequence = ['#0000FF', '#00FF00','#FF0000','#FFFF00'], text = 'QUANTIDADE')

    return fig_bar


@app.callback(Output(component_id='setor', component_property='figure'),
              Input(component_id='botoes_setor', component_property='value'))

def update_graph_2(a):

    df_quant_setor_copy = df_quant_setor.copy()
    df_quant_setor_copy = df_quant_setor_copy[df_quant_setor_copy['SETOR'].isin(a)]

    fig_bar_2 = px.bar(df_quant_setor_copy, x = 'SETOR', y = 'QUANTIDADE', color = 'STATUS',
                       color_discrete_sequence = ['#00FF00','#FF0000','#FFFF00','#0000FF'], text = 'QUANTIDADE')

    return fig_bar_2

if __name__ == '__main__':
    app.run_server(debug=True)
