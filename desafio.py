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

    fig_visualizacao = px.bar(df, x = 'Título',  y='Visualizações', title='Visualizações por vídeo')
    fig_curtidas = px.bar(df, x='Título', y='Curtidas', title='Curtidas por vídeo')
    fig_comentarios = px.bar(df, x='Título', y='Comentários', title='Comentários por vídeo')

    fig_relacao = px.scatter(df, x='Curtidas', y='Comentários', text='Título', title='Curtidas vs Comentários por Vídeo',
    labels={'Curtidas': 'Número de Curtidas', 'Comentários': 'Número de Comentários'})
    fig_relacao.update_traces(textposition='top center')

    fig_tempoPorVisu = px.line(df, x='Data', y='Visualizações', title='Evolução das Visualizações por Data')

    top10 = df.sort_values(by='Visualizações', ascending=False).head(10)
    fig_top10 = px.bar(top10, x='Título', y='Visualizações', title='Top 10 Vídeos Mais Visualizados')

    fig_viz_likes = px.scatter(top10, x='Visualizações', y='Curtidas', text='Título', title='Visualizações vs Curtidas')

    df['Engajamento (%)'] = ((df['Curtidas'] + df['Comentários']) / df['Visualizações']) * 100
    fig_engajamento = px.bar(df, x='Título', y='Engajamento (%)', title='Engajamento Relativo por Vídeo')

    app.layout = html.Div([
         html.H1("Dashboard YouTube - Highlights F1 2024"),
        dcc.Graph(figure= fig_visualizacao),
        dcc.Graph(figure=fig_curtidas),
        dcc.Graph(figure=fig_comentarios),
        dcc.Graph(figure=fig_relacao),
        dcc.Graph(figure=fig_tempoPorVisu),
        dcc.Graph(figure=fig_top10),
        dcc.Graph(figure=fig_viz_likes),
        dcc.Graph(figure= fig_engajamento)
    ])
    app.run(debug=True)

if __name__ == '__main__':
    videos = buscar_videos(youtube, playlist_id)
    stats = estatisticas(youtube, videos)

    df = dataFreme(videos, stats)
    dashboard(df)