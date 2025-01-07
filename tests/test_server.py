import pytest
import socket
import threading
import time
from src.server import ChatServer

@pytest.fixture
def chat_server():
    """
    Fixture para configurar un servidor de chat para pruebas
    
    Crea un servidor de chat en un puerto específico para pruebas
    y lo inicia en un hilo separjado
    
    :return: Instancia del servidor de chat
    """
    server = ChatServer(host='localhost', port=55556)
    server.start_server()
    server_thread = threading.Thread(target=server.receive)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.1)  # Dar tiempo para que el servidor inicie
    return server

### Req 1 ######
def test_inicializacion_servidor(chat_server):
    """
    Prueba la inicialización correcta del servidor
    
    Verifica que:
    - El servidor se crea correctamente
    - No hay clientes conectados inicialmente
    """
    assert chat_server.server is not None
    assert len(chat_server.clients) == 0

def test_conexion_cliente(chat_server):
    """
    Prueba la conexión de un cliente al servidor
    
    Verifica que:
    - Un cliente puede conectarse al servidor
    - El servidor solicita un nickname
    - El cliente puede enviar un nickname
    - El servidor confirma la conexión
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 55556))
    
    # El servidor debe solicitar un nickname
    assert client.recv(1024).decode('utf-8') == 'NICK'
    
    # Enviar nickname
    client.send('UsuarioPrueba'.encode('utf-8'))
    
    # Verificar mensaje de conexión
    assert 'Conectado al servidor!' in client.recv(1024).decode('utf-8')
    
    client.close()

def test_envio_mensaje_broadcast(chat_server):
    """
    Prueba el envío de mensajes entre múltiples clientes
    
    Verifica que:
    - Los mensajes se retransmiten correctamente
    - Todos los clientes conectados reciben el mensaje
    """
    # Simular conexión de múltiples clientes
    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client1.connect(('localhost', 55556))
    client2.connect(('localhost', 55556))
    
    # Manejar intercambio de nicknames
    client1.recv(1024)  # Solicitud de NICK
    client1.send('Usuario1'.encode('utf-8'))
    client2.recv(1024)  # Solicitud de NICK
    client2.send('Usuario2'.encode('utf-8'))
    
    # Enviar un mensaje desde client1
    client1.send('¡Hola a todos!'.encode('utf-8'))
    
    # Verificar si client2 recibe el mensaje
    message = client2.recv(1024).decode('utf-8')
    assert '¡Hola a todos!' in message
    
    client1.close()
    client2.close()

def test_desconexion_cliente(chat_server):
    """
    Prueba el manejo de desconexiones de clientes
    
    Verifica que:
    - El servidor maneja correctamente la desconexión de un cliente
    - Otros clientes no se ven afectados por la desconexión
    """
    # Conectar múltiples clientes
    clients = []
    for i in range(3):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 55556))
        client.recv(1024)  # Solicitud de NICK
        client.send(f'Usuario{i}'.encode('utf-8'))
        clients.append(client)
    
    # Verificar número inicial de clientes
    assert len(chat_server.clients) == 3
    
    # Desconectar un cliente
    clients[0].close()
    time.sleep(0.1)  # Dar tiempo para procesar la desconexión
    
    # Verificar que el número de clientes se redujo
    assert len(chat_server.clients) == 2
    
    # Cerrar clientes restantes
    for client in clients[1:]:
        client.close()