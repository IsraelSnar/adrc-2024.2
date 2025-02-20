from flask import Flask, render_template
import socket
import listar

app = Flask(__name__)

@app.route('/')
def home():
    host = ''
    try:
        host = socket.gethostname()
    except:
        host = 'erro ao pegar hostname'

    return render_template('index.html', host=host)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
