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
        status = stats.get(video_id, {})

        dados.append({
            'Título': titulo,
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

    app.layout = html.Div([
         html.H1("Dashboard YouTube - Highlights F1 2024"),
        dcc.Graph(figure= fig_visualizacao),
        dcc.Graph(figure=fig_curtidas),
        dcc.Graph(figure=fig_comentarios)
    ])
    app.run(debug=True)

if __name__ == '__main__':
    videos = buscar_videos(youtube, playlist_id)
    stats = estatisticas(youtube, videos)

    df = dataFreme(videos, stats)
    dashboard(df)

    print("Vídeos na playlist:")

    for item in videos:
        snippet = item['snippet']
        video_id = snippet['resourceId'] ['videoId']
        titulo = snippet['title']

        status= stats.get(video_id, {})
        vizualização = status.get('viewCount', 'N/A')
        curtidas = status.get('likeCount', 'N/A')
        comentarios = status.get('commentCount', 'N/A')

        print(f"Título: {titulo}")
        print(f"Visualizações: {vizualização}")
        print(f"Curtidas: {curtidas}")
        print(f"Comentários: {comentarios}")
        print("---")