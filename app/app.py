from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Permitindo todas as origens para fins de teste

# Conjunto para armazenar clientes conectados
clientes = set()

@socketio.on('message')
def handle_message(data):
    nome_usuario = data['nome_usuario']
    mensagem = data['mensagem']

    # Informa a todos os clientes sobre a nova mensagem
    socketio.emit('message', {'nome_usuario': nome_usuario, 'mensagem': mensagem}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print('Novo cliente conectado')


@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

if __name__ == '__main__':
    socketio.run(app, host='www.trabalhofinalfrc.com', port=5000)
