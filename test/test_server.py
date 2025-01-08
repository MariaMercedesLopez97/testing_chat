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
    y lo inicia en un hilo separado
    
    :return: Instancia del servidor de chat
    """
    server = ChatServer(host='localhost', port=55556)
    server.start_server()
    server_thread = threading.Thread(target=server.receive)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.1)  # Dar tiempo para que el servidor inicie
    yield server
    # Limpieza después de cada prueba
    for client in server.clients[:]:
        server.remove_client(client)
    server.server.close()

### Pruebas Unitarias Básicas ###
def test_inicializacion_servidor(chat_server):
    """Prueba la inicialización correcta del servidor"""
    assert chat_server.server is not None
    assert len(chat_server.clients) == 0
    assert len(chat_server.nicknames) == 0

### Pruebas de Conexión ###
def test_conexion_cliente(chat_server):
    """Prueba la conexión de un cliente al servidor"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 55556))
    
    # Verificar solicitud de nickname
    assert client.recv(1024).decode('utf-8') == 'NICK'
    
    # Enviar nickname
    nickname = 'UsuarioPrueba'
    client.send(nickname.encode('utf-8'))
    
    # Verificar mensaje de bienvenida
    response = client.recv(1024).decode('utf-8')
    assert 'Conectado al servidor!' in response
    
    # Verificar que el cliente fue agregado al servidor
    assert len(chat_server.clients) == 1
    assert nickname in chat_server.nicknames
    
    client.close()

### Pruebas de Comunicación ###
def test_envio_mensaje_broadcast(chat_server):
    """
    Prueba el envío de mensajes entre múltiples clientes
    """
    # Conectar dos clientes
    clients = []
    for i in range(2):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 55556))
        client.recv(1024)  # NICK
        client.send(f'Usuario{i}'.encode('utf-8'))
        client.recv(1024)  # Mensaje de bienvenida
        clients.append(client)
    
    # Enviar mensaje desde el primer cliente
    mensaje = "¡Hola a todos!"
    clients[0].send(mensaje.encode('utf-8'))
    
    # Verificar que el segundo cliente recibe el mensaje
    received = clients[1].recv(1024).decode('utf-8')
    assert mensaje in received
    
    for client in clients:
        client.close()

##Pruebas de Múltiples Clientes
def test_mensajes_simultaneos(chat_server):
    """Prueba de integración: múltiples clientes enviando mensajes simultáneamente"""
    clientes = []
    mensajes_recibidos = {i: [] for i in range(3)}
    
    def recibir_mensajes(client_id, client):
        while True:
            try:
                msg = client.recv(1024).decode('utf-8')
                if msg:
                    mensajes_recibidos[client_id].append(msg)
            except:
                break
    # Conectar múltiples clientes y verificar mensajes
    for i in range(3):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 55556))

        client.recv(1024)  # NICK
        client.send(f'Usuario{i}'.encode('utf-8'))
        client.recv(1024)  # Mensaje de bienvenida
        clientes.append(client)
        
        thread = threading.Thread(target=recibir_mensajes, args=(i, client))
        thread.daemon = True
        thread.start()
    
    # Enviar mensajes desde todos los clientes
    mensajes_enviados = []
    for i, client in enumerate(clientes):
        mensaje = f"Mensaje de prueba {i}"
        mensajes_enviados.append(mensaje)
        client.send(mensaje.encode('utf-8'))
    
    time.sleep(0.5)
    
    # Verificar recepción de mensajes
    for i in range(3):
        for mensaje in mensajes_enviados:
            if f"Usuario{i}" not in mensaje:
                assert any(mensaje in msg for msg in mensajes_recibidos[i])
    
    for client in clientes:
        client.close()

### Pruebas de Desconexión ###
def test_desconexion_normal(chat_server):
    """Prueba la desconexión normal de un cliente"""
    # Conectar cliente
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 55556))
    client.recv(1024)  # NICK
    client.send('Usuario1'.encode('utf-8'))
    client.recv(1024)  # Mensaje de bienvenida
    
    # Verificar conexión
    assert len(chat_server.clients) == 1
    
    # Desconexión normal
    client.close()
    time.sleep(0.1)
    
    # Verificar que el cliente fue removido
    assert len(chat_server.clients) == 0
    assert 'Usuario1' not in chat_server.nicknames

###Prueba de Desconexiones Abruptas###
def test_desconexion_abrupta(chat_server):
    """Prueba el manejo de desconexiones abruptas de clientes"""
    clientes = []
    
    # Conectar 4 clientes
    for i in range(4):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 55556))
        #... Conexion de clientes ...

        client.recv(1024)  # NICK
        client.send(f'Usuario{i}'.encode('utf-8'))
        client.recv(1024)  # Mensaje de bienvenida
        clientes.append(client)
    
    # Verificar conexiones iniciales
    assert len(chat_server.clients) == 4
    
    # Desconexion abrupta y verificarcion del cliente 1
    clientes[1].close()
    time.sleep(0.1)
    
    # Verificar que el servidor eliminó al cliente
    assert len(chat_server.clients) == 3
    assert f'Usuario1' not in chat_server.nicknames
    
    # Enviar mensaje desde cliente 0
    mensaje = "Mensaje después de desconexión"
    clientes[0].send(mensaje.encode('utf-8'))
    
    # Verificar que los clientes restantes reciben el mensaje
    mensaje_recibido = clientes[2].recv(1024).decode('utf-8')
    assert mensaje in mensaje_recibido
    
    # Verificar que el servidor sigue funcionando
    assert chat_server.server.fileno() != -1
    
    # Limpiar
    for client in clientes:
        try:
            client.close()
        except:
            pass

### Pruebas de Casos Límite ###
def test_multiples_conexiones_simultaneas(chat_server):
    """
    Prueba el manejo de múltiples conexiones simultáneas
    """
    clientes = []
    num_clientes = 10
    
    # Conectar varios clientes rápidamente
    for i in range(num_clientes):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 55556))
        client.recv(1024)  # NICK
        client.send(f'Usuario{i}'.encode('utf-8'))
        client.recv(1024)  # Mensaje de bienvenida
        clientes.append(client)
    
    # Verificar que todos los clientes se conectaron correctamente
    assert len(chat_server.clients) == num_clientes
    
    # Limpiar
    for client in clientes:
        client.close()
