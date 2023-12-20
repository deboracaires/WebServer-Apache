import asyncio
import websockets

clientes = set()

async def enviar_mensagem_para_todos(mensagem):
    # Cria uma cópia do conjunto para evitar RuntimeError durante a iteração
    clientes_atuais = clientes.copy()

    # Lista de clientes a serem removidos (se houver desconexões)
    clientes_a_remover = []

    # Envia a mensagem para todos os clientes
    for nome_usuario, cliente_ws, _, _ in clientes_atuais:
        try:
            await cliente_ws.send(mensagem)
        except websockets.exceptions.ConnectionClosedError:
            # Adiciona à lista de clientes a serem removidos se a conexão estiver fechada
            clientes_a_remover.append((nome_usuario, cliente_ws))

    # Remove os clientes desconectados
    for cliente_a_remover in clientes_a_remover:
        clientes.remove(cliente_a_remover)

async def transmitir_video(nome_usuario, video_data):
    # Enviar a mensagem para todos os clientes com o nome do remetente
    await enviar_mensagem_para_todos(f"{nome_usuario} enviou um vídeo.")
    await enviar_mensagem_para_todos(f"VIDEO:{video_data}")

async def servidor(websocket, caminho):
    try:
        # Solicita ao cliente que forneça um nome de usuário único
        nome_usuario = await websocket.recv()
        print(f"Novo usuário conectado: {nome_usuario}")

        # Adiciona o novo cliente à lista de clientes
        clientes.add((nome_usuario, websocket, "Online", False))

        # Informa a todos os clientes que um novo usuário entrou no chat
        await enviar_mensagem_para_todos(f"STATUS:{nome_usuario}:Online")

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
    finally:
        # Remove o cliente da lista quando a conexão é encerrada
        clientes.remove((nome_usuario, websocket, "Online", False))
        await enviar_mensagem_para_todos(f"STATUS:{nome_usuario}:Offline")

start_server = websockets.serve(servidor, "localhost", 8765)

print("Servidor WebSocket iniciado. Aguardando conexões...")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()