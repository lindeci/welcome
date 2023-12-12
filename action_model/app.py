from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet
import os
import whisper
import zhconv
model = whisper.load_model("large")


eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('audio')
def handle_audio(data):
    # Handle audio data here, and save it to a file
    with open('audio.wav', 'wb') as f:
        f.write(data)
    result = model.transcribe("audio.wav")
    simplified_text = zhconv.convert(result["text"], 'zh-cn')
    socketio.emit('saved',simplified_text)

if __name__ == '__main__':
        socketio.run(app, host='0.0.0.0', port=5000, keyfile='key.pem', certfile='cert.pem')