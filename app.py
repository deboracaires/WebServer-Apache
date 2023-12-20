from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

#---------------ASSUNTOS GERAIS---------------#
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('login')
def handle_login(data):
    name = data['name']
    senha = data['senha']
    topic = data['topic']

    user = User.query.filter_by(name=name, password=senha).first()
    
    if not user:
        new_user = User(name=name, password=senha)
        db.session.add(new_user)
        db.session.commit()

    if topic == 'culinaria':
        socketio.emit('redirect', '/culinaria')  
    elif topic == 'futebol':
        socketio.emit('redirect', '/futebol')
    elif topic == 'politica':
        socketio.emit('redirect', '/politica')
    elif topic == 'religiao':
        socketio.emit('redirect', '/religiao')
    else:
        socketio.emit('redirect', '/')

@socketio.on('message')
def handle_message(data):
    name = request.sid  # Pega o ID da sessão como nome (pode ser personalizado conforme necessário)
    message = data['message']
    topic = data['topic']
    print(f'Received message from {name} in {topic}: {message}')
    socketio.emit(f'message_{topic}', {'name': name, 'message': message})
 #---------------ASSUNTOS GERAIS---------------#

#----------------Politica----------------------#
@app.route('/politica')
def politica():
    return render_template('politica.html')

@socketio.on('message_politica')
def handle_message_culinaria(data):
    name = data['name']
    message = data['message']
    socketio.emit('message_politica', {'name': name, 'message': message})
#-----------------Politica---------------------#


#----------------Futebol----------------------#
@app.route('/futebol')
def futebol():
    return render_template('futebol.html')

@socketio.on('message_futebol')
def handle_message_futebol(data):
    name = data['name']
    message = data['message']
    socketio.emit('message_futebol', {'name': name, 'message': message})

#-----------------Futebol---------------------#

#----------------Culinaria----------------------#
@app.route('/culinaria')
def culinaria():
    return render_template('culinaria.html')

@socketio.on('message_culinaria')
def handle_message_culinaria(data):
    name = data['name']
    message = data['message']
    socketio.emit('message_culinaria', {'name': name, 'message': message})

#-----------------Culinaria---------------------#



#----------------Religiao----------------------#
@app.route('/religiao')
def religiao():
    return render_template('religiao.html')

@socketio.on('message_religiao')
def handle_message_culinaria(data):
    name = data['name']
    message = data['message']
    socketio.emit('message_religiao', {'name': name, 'message': message})
#-----------------Religiao---------------------#


if __name__ == '__main__':
    socketio.run(app, debug=True)
