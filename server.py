from flask import Flask
from threading import Thread

app = Flask("")

@app.route('/')
def main():
  return "botが起動しました"

def run():
  app.run(host="0.0.0.0", port=8080)

def start():
  server = Thread(target=run)
  server.start()