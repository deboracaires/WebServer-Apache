from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
#---------------ASSUNTOS GERAIS---------------#
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)
    socketio.emit('message', msg)
 #---------------ASSUNTOS GERAIS---------------#

#----------------Politica----------------------#
@app.route('/politica')
def politica():
    return render_template('politica.html')

@socketio.on('message_politica')
def handle_message_politica(msg):
    print('Received political message: ' + msg)
    socketio.emit('message_politica', msg)
#-----------------Politica---------------------#


#----------------Futebol----------------------#
@app.route('/futebol')
def futebol():
    return render_template('futebol.html')

@socketio.on('message_futebol')
def handle_message_futebol(msg):
    print('Received futebol message: ' + msg)
    socketio.emit('message_futebol', msg)
#-----------------Futebol---------------------#

#----------------Religiao----------------------#
@app.route('/religiao')
def religiao():
    return render_template('religiao.html')

@socketio.on('message_religiao')
def handle_message_religiao(msg):
    print('Received religiao message: ' + msg)
    socketio.emit('message_religiao', msg)
#-----------------Religiao---------------------#


#----------------Culinaria----------------------#
@app.route('/culinaria')
def culinaria():
    return render_template('culinaria.html')

@socketio.on('message_culinaria')
def handle_message_culinaria(msg):
    print('Received culinaria message: ' + msg)
    socketio.emit('message_culinaria', msg)
#-----------------Culinaria---------------------#



if __name__ == '__main__':
    socketio.run(app, debug=True)
