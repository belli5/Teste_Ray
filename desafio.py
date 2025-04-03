from googleapiclient.discovery import build

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



if __name__ == '__main__':
    videos = buscar_videos(youtube, playlist_id)
    stats = estatisticas(youtube, videos)

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