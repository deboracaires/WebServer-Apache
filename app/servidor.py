import asyncio
import websockets
import json

clientes = []

async def enviar_mensagem_para_todos(mensagem):
    # Cria uma cópia da lista para evitar RuntimeError durante a iteração
    clientes_atuais = [cliente for cliente in clientes if cliente['status'] != 'Offline']

    # Lista de clientes a serem removidos (se houver desconexões)
    clientes_a_remover = []

    # Envia a mensagem para todos os clientes
    for cliente in clientes_atuais:
        try:
            if cliente['websocket'].closed:
                continue

            await cliente['websocket'].send(mensagem)
        except websockets.exceptions.ConnectionClosedError:
            # Adiciona à lista de clientes a serem removidos se a conexão estiver fechada
            clientes_a_remover.append(cliente)

    # Remove os clientes desconectados
    for cliente in clientes_a_remover:
        atualiza_status(cliente['nome_usuario'], "Offline")

async def transmitir_video(nome_usuario, video_data):
    # Enviar a mensagem para todos os clientes com o nome do remetente
    await enviar_mensagem_para_todos(f"{nome_usuario} enviou um vídeo.")
    await enviar_mensagem_para_todos(f"VIDEO:{video_data}")

def atualiza_status(nome_usuario, new_status):
    for cliente in clientes:
        if cliente['nome_usuario'] == nome_usuario:
            cliente['status'] = new_status
            break

def atualiza_socket(nome_usuario, new_socket):
    for cliente in clientes:
        if cliente['nome_usuario'] == nome_usuario:
            cliente['websocket'] = new_socket
            break

def cliente_cadastrado(nome_usuario):
    for cliente in clientes:
        if cliente['nome_usuario'] == nome_usuario:
            return True

    return False

def lista_clientes():
    return [{'nome_usuario': cliente['nome_usuario'], 'status': cliente['status']} for cliente in clientes]

async def servidor(websocket, caminho):
    try:
        # Solicita ao cliente que forneça um nome de usuário único
        nome_usuario = await websocket.recv()

        if cliente_cadastrado(nome_usuario):
            atualiza_status(nome_usuario, "Online")
            atualiza_socket(nome_usuario, websocket)
            print(clientes)
        else:
            print(f"Novo usuário conectado: {nome_usuario}")

            # Adiciona o novo cliente à lista de clientes
            clientes.append({'nome_usuario': nome_usuario, 'websocket': websocket, 'status': 'Online', 'busy': False})

        # Informa a todos os clientes que um novo usuário entrou no chat
        await enviar_mensagem_para_todos(f"STATUS:{json.dumps(lista_clientes())}")

        # Mantém a conexão aberta
        async for mensagem in websocket:
            # Verifica se a mensagem é um vídeo
            if mensagem.startswith("VIDEO:"):
                await transmitir_video(nome_usuario, mensagem[6:])
            else:
                # Envia a mensagem para todos os clientes
                await enviar_mensagem_para_todos(f"{nome_usuario}: {mensagem}")
                print(f"Recebido de {nome_usuario}: {mensagem}")  # Adiciona esta linha para imprimir no console

    except websockets.exceptions.ConnectionClosedError:
        print(f"Conexão fechada inesperadamente com {nome_usuario}.")
    # except websockets.exceptions.ConnectionClosedOK:
    #     print(f"Conexão fechada OK com {nome_usuario}.")
    finally:
        # Remove o cliente da lista quando a conexão é encerrada
        # clientes.remove({'nome_usuario': nome_usuario, 'websocket': websocket, 'status': 'Online', 'busy': False})
        atualiza_status(nome_usuario, "Offline")
        await enviar_mensagem_para_todos(f"STATUS:{json.dumps(lista_clientes())}")

start_server = websockets.serve(servidor, "localhost", 8765)

print("Servidor WebSocket iniciado. Aguardando conexões...")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
