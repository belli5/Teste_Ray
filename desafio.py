from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

API_KEY = 'AIzaSyCvbxSrVjyh0Dq11kXv23bdyJ2gGxhRHL0'
youtube = build('youtube', 'v3', developerKey=API_KEY)

playlist_id = 'PLfoNZDHitwjUv0pjTwlV1vzaE0r7UDVDR'

def buscar_videos(youtube, playlist_id):
    resultados = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=25
    ).execute()
    return resultados['items']

def estatisticas(youtube, videos):
    video_ids = [item['snippet']['resourceId']['videoId'] for item in videos]

    resposta = youtube.videos().list(
        part= 'statistics',
        id=','.join(video_ids)
    ).execute()
    stats = {} #dicionario 
    for item in resposta['items']: #percorre cada video da lista
        stats[item['id']] = item['statistics'] #para cada video salva no dicionario suas estatisticas 
    return stats

def dataFreme(videos, stats):
    dados = []

    for item in videos:
        snippet = item['snippet']
        video_id = snippet['resourceId'] ['videoId']
        titulo = snippet['title']
        data = snippet['publishedAt'][:10]
        status = stats.get(video_id, {})

        dados.append({
            'Título': titulo,
            'Data': data,
            'Visualizações': int(status.get('viewCount', 0)),
            'Curtidas': int(status.get('likeCount', 0)),
            'Comentários': int(status.get('commentCount', 0)),
        })
    return pd.DataFrame(dados)

def dashboard(df):

    app = Dash(__name__)

    fig_curtidas = px.bar(df, x='Título', y='Curtidas', title='Curtidas por vídeo')
    fig_comentarios = px.bar(df, x='Comentários', y='Título', orientation='h', title='Comentários por vídeo')

    fig_relacao = px.scatter(df, x='Curtidas', y='Comentários', text='Título', title='Curtidas vs Comentários por Vídeo',
    labels={'Curtidas': 'Número de Curtidas', 'Comentários': 'Número de Comentários'})
    fig_relacao.update_traces(textposition='top center')

    fig_tempoPorVisu = px.line( df, x='Data', y='Visualizações', hover_name='Título', title='Evolução das Visualizações por Data', markers=True)
    media = df['Visualizações'].mean()
    fig_tempoPorVisu.add_hline(y=media, line_dash="dash", line_color="red", annotation_text=f"Média: {int(media):,} views", annotation_position="bottom right")

    top10 = df.sort_values(by='Visualizações', ascending=False).head(10)
    top10['Título Rankeado'] = [f"{i+1}º - {titulo}" for i, titulo in enumerate(top10['Título'])]
    fig_top10_pizza = px.pie(top10, names='Título Rankeado', values='Visualizações', title='Distribuição de Visualizações - Top 10 Vídeos (Com Ranking)')
    fig_top10_pizza.update_traces(textinfo='percent+label')

    fig_viz_likes = px.scatter(top10, x='Visualizações', y='Curtidas', text='Título', title='Visualizações vs Curtidas')

    df['Engajamento (%)'] = ((df['Curtidas'] + df['Comentários']) / df['Visualizações']) * 100
    fig_engajamento = px.bar(df.sort_values(by='Engajamento (%)', ascending=False), x='Título', y='Engajamento (%)', title='Engajamento Relativo por Vídeo (Ordenado)')

    df['Faixa de Views'] = pd.cut(df['Visualizações'], bins=3, labels=['Pouco visto', 'Médio', 'Muito visto'])

    fig_bar_engajamento = px.bar(df.sort_values(by='Visualizações'), x='Título', y='Engajamento (%)', color='Faixa de Views', title='Engajamento Relativo por Vídeo (Classificado por Visualizações)')

    app.layout = html.Div([
        html.H1("Dashboard YouTube - Highlights F1 2024"),
        html.P("Esse dashboard apresenta uma análise dos vídeos de highlights da temporada 2024 de F1 publicados no canal oficial. Abaixo, exploramos os vídeos com maior desempenho em visualizações, curtidas e comentários."),
        html.Hr(),

        html.P("Vídeos com nomes de circuitos específicos e recentes atraem mais curtidas — possivelmente por estarem atrelados a corridas populares ou finais emocionantes. Como é o caso do GP do Canadá, Áustria, São Paulo, Monaco e Miami "),
        dcc.Graph(figure=fig_curtidas),

        html.P("Vídeos com momentos polêmicos, acidentes ou finais surpreendentes tendem a gerar mais comentários — demonstrando maior envolvimento emocional do público. Como é o caso do GP da Hungria, que teve a polemica da McLaren"),
        dcc.Graph(figure=fig_comentarios),

         html.P("Qual é a Correlação entre Curtidas e Comentarios? Os vídeos mais curtidos são os mais Comentados ou os mais Comentados são os mais curtidos?"),
        html.P(["Existe uma ", html.Strong("correlação positiva"), " clara entre curtidas e comentários. Quanto mais curtidas um vídeo tem, maior tende a ser seu número de comentários."]),
        html.P("Alguns vídeos, como o GP da Hungria e o GP da Austrália, se destacam acima da linha de tendência, indicando que geraram comentários além do esperado para o número de curtidas."),
        dcc.Graph(figure=fig_relacao),

        html.P("Os circuitos mais tradicionais ou com maior apelo midiático (Austrália, Mônaco, São Paulo) tendem a gerar maior curiosidade e tráfego orgânico no canal. Essas corridas provavelmente foram marcantes na temporada."),
        dcc.Graph(figure=fig_top10_pizza),

        html.P("Os vídeos mais visualizados também são os mais curtidos?"),
        html.P("Curtidas não dependem apenas do número de visualizações, mas também da qualidade percebida, emoção ou relevância da corrida. Corridas mais intensas ou com desfechos inesperados tendem a gerar mais likes por view."),
        dcc.Graph(figure=fig_viz_likes),

        html.P("Falando em visualizações, o interesse do público aumentou ou caiu ao longo da temporada?"),
        html.P("Corridas lançadas no início da temporada de 2024 despertaram mais interesse e geraram visualizações muito acima da média. Já no fim do ano, o engajamento caiu, sugerindo que o pico de atenção ocorre nos primeiros meses"),
        html.P("A linha vermelha mostra a média de visualizações ao longo do tempo. Picos acima da média indicam corridas que despertaram mais atenção do público."),
        dcc.Graph(figure=fig_tempoPorVisu),

        html.P("Vídeos com alto engajamento nem sempre são os mais visualizados!"),
        html.P("GP de Miami e GP da Grã-Bretanha aparecem no topo em engajamento mesmo sem estarem entre os mais visualizados. Isso sugere que esses vídeos provocaram forte reação emocional, levando o público a interagir mais — seja curtindo ou comentando."),
        dcc.Graph(figure= fig_engajamento),

        html.P("O maior engajamento está no grupo Médio! "),
        html.P("Os dois maiores picos de engajamento estão nos vídeos com visualizações intermediárias. Isso pode indicar que corridas intensas ou emocionantes, mesmo com público menor, ativaram mais o engajamento emocional (likes + comentários)."),
        dcc.Graph(figure=fig_bar_engajamento),

        encerramento()
    ])
    app.run(debug=True)

def encerramento():
    return html.Div([
        html.H2("🏁 Encerramento: A Temporada Além da Pista"),
        html.P("Ao longo da temporada 2024 da Fórmula 1, não foi apenas nas curvas e ultrapassagens que as emoções aconteceram — elas também explodiram nos bastidores digitais do YouTube."),
        html.P("🔍 Nossa análise mergulhou fundo nas reações do público aos vídeos de highlights, revelando que:"),
        html.Ul([
            html.Li("Corridas populares como Austrália, Mônaco e São Paulo garantiram milhões de visualizações, mas..."),
            html.Li("...foi em momentos mais intensos, inesperados ou polêmicos — como o GP da Hungria — que o verdadeiro engajamento aconteceu.")
        ]),
        html.P("✨ Curtidas e comentários mostraram que, quando uma corrida toca o emocional do torcedor, ela transcende os números. Às vezes, um vídeo 'médio' em audiência deixa uma marca maior que os gigantes em visualizações."),
        html.P("📈 A jornada também mostrou que o interesse do público flutua ao longo da temporada, com picos iniciais e quedas no fim do ano — talvez o reflexo da narrativa esportiva se esgotando, ou da previsibilidade crescendo."),
        html.Blockquote("🎯 E o que aprendemos com tudo isso? Que no mundo digital, mais do que ser visto, é preciso ser sentido. O público não quer apenas assistir corridas — ele quer viver as corridas."),
        html.H3("🏆 Obrigado por acompanhar essa análise!"),
        html.P("Esse dashboard é mais do que números: É uma forma de ouvir a voz dos fãs, entender seus sentimentos e mapear o impacto que o esporte gera fora das pistas."),
    ], style={
        'marginTop': '50px',
        'padding': '20px',
        'backgroundColor': '#f9f9f9',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
        'fontFamily': 'Arial, sans-serif'
    })

if __name__ == '__main__':
    videos = buscar_videos(youtube, playlist_id)
    stats = estatisticas(youtube, videos)

    df = dataFreme(videos, stats)
    dashboard(df)