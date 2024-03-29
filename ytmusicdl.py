from youtubesearchpython import VideosSearch
import pytube
import os

def download(query: str):
  id = VideosSearch(query, limit = 1).result()["result"][0]["id"]
  yt = pytube.YouTube(f"https://youtu.be/{id}")
  path = yt.streams.filter(only_audio=True)[0].download()
  if os.path.isfile("music.mp3"):
    os.remove("music.mp3")
  os.rename(path, "music.mp3")