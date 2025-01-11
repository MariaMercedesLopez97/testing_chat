import pytest
import socket
import threading
import time

from server import ChatServer

@pytest.fixture
def chat_server():
    """Fixture para configurar un servidor de chat para pruebas"""
    server = ChatServer(host='localhost', port=55556)
    server.start_server()
    
    # Iniciar el servidor en un hilo separado
    server_thread = threading.Thread(target=server.run)
    server_thread.daemon = True
    server_thread.start()
    
    time.sleep(0.1)  # Dar tiempo para que el servidor inicie
    yield server
    
    # Limpieza después de cada prueba
    for client in server.clients[:]:
        server.remove_client(client)
    server.server.close()

### Pruebas Unitarias Básicas (Req 1) ###
def test_inicializacion_servidor(chat_server):
    """Prueba la inicialización correcta del servidor"""
    assert chat_server.server is not None
    assert len(chat_server.clients) == 0
    assert len(chat_server.nicknames) == 0

def test_broadcast(chat_server):
    """Prueba la función de broadcast"""
    # Crear clientes de prueba
    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar clientes
    client1.connect(('localhost', 55556))
    client2.connect(('localhost', 55556))
    
    # Proceso de conexión
    for client in [client1, client2]:
        assert client.recv(1024).decode('utf-8') == 'NICK'
        client.send('TestUser'.encode('utf-8'))
        client.recv(1024)  # Mensaje de bienvenida
    
    # Prueba de broadcast
    mensaje = "Mensaje de prueba"
    chat_server.broadcast(mensaje.encode('utf-8'))
    
    # Verificar que ambos clientes reciben el mensaje
    assert mensaje in client1.recv(1024).decode('utf-8')
    assert mensaje in client2.recv(1024).decode('utf-8')
    
    client1.close()
    client2.close()

### Pruebas de Integración (Req 3) ###
def test_multiple_clients_communication(chat_server):
    """Prueba la comunicación entre múltiples clientes"""
    clients = []
    messages_received = []
    
    def client_receiver(client, index):
        while True:
            try:
                msg = client.recv(1024).decode('utf-8')
                if msg and "Mensaje de prueba" in msg:
                    messages_received.append(msg)
                    break
            except:
                break
    
    # Conectar 3 clientes
    for i in range(3):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 55556))
        client.recv(1024)  # NICK
        client.send(f'User{i}'.encode('utf-8'))
        client.recv(1024)  # Bienvenida
        clients.append(client)
        
        # Iniciar thread para recibir mensajes
        thread = threading.Thread(target=client_receiver, args=(client, i))
        thread.daemon = True
        thread.start()
    
    # Enviar mensaje desde el primer cliente
    test_message = "Mensaje de prueba"
    clients[0].send(test_message.encode('utf-8'))
    
    time.sleep(0.5)
    
    # Verificar que los otros clientes recibieron el mensaje
    assert len(messages_received) == 2
    
    for client in clients:
        client.close()

### Pruebas de Desconexión Abrupta (Req 4) ###
def test_client_abrupt_disconnect(chat_server):
    """Prueba el manejo de desconexiones abruptas"""
    clients = []
    
    # Conectar 3 clientes
    for i in range(3):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 55556))
        client.recv(1024)  # NICK
        client.send(f'User{i}'.encode('utf-8'))
        client.recv(1024)  # Bienvenida
        clients.append(client)
    
    # Desconectar abruptamente el segundo cliente
    clients[1].close()
    time.sleep(0.1)
    
    # Verificar que el servidor sigue funcionando
    test_message = "Mensaje post desconexión"
    clients[0].send(test_message.encode('utf-8'))
    
    # Verificar que el tercer cliente recibe el mensaje
    response = clients[2].recv(1024).decode('utf-8')
    assert test_message in response
    
    # Verificar estado del servidor
    assert len(chat_server.clients) == 2
    
    for client in clients:
        try:
            client.close()
        except:
            pass