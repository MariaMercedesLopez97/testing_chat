import pytest
import socket
import threading
import time
from src.client import ChatClient
from src.server import ChatServer

@pytest.fixture
def chat_server():
    """
    Fixture para configurar un servidor de chat para pruebas
    """
    server = ChatServer(host='localhost', port=55557)
    server.start_server()
    server_thread = threading.Thread(target=server.receive)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.1)  # Dar tiempo para que el servidor inicie
    return server

### Req 1###
def test_client_connection(chat_server):
    """
    Prueba la conexión de un cliente al servidor
    """
    client = ChatClient(host='localhost', port=55557)
    connection = client.connect('TestUser')
    
    # Verificar que la conexión se establece correctamente
    assert connection is not None
    connection.close()

def test_client_send_message(chat_server):
    """
    Prueba el envío de mensajes de un cliente
    """
    client1 = ChatClient(host='localhost', port=55557)
    client2 = ChatClient(host='localhost', port=55557)
    
    conn1 = client1.connect('User1')
    conn2 = client2.connect('User2')
    
    # Enviar un mensaje desde client1
    client1.send(conn1, 'Hola, este es un mensaje de prueba')
    
    # Recibir mensaje en client2
    message = conn2.recv(1024).decode('utf-8')
    
    # Verificar que el mensaje se recibe correctamente
    assert 'Hola, este es un mensaje de prueba' in message
    
    conn1.close()
    conn2.close()

def test_multiple_client_connections(chat_server):
    """
    Prueba la conexión de múltiples clientes
    """
    clients = []
    connections = []
    
    # Conectar 5 clientes
    for i in range(5):
        client = ChatClient(host='localhost', port=55557)
        conn = client.connect(f'User{i}')
        clients.append(client)
        connections.append(conn)
    
    # Verificar que todos los clientes están conectados
    assert len(chat_server.clients) == 5
    
    # Cerrar todas las conexiones
    for conn in connections:
        conn.close()

### Req 2###
#Verificar la validación de nicknames
def test_nickname_validation():
    """
    Prueba la validación de nicknames
    - No debe permitir nicknames vacíos
    - No debe permitir nicknames con espacios
    - No debe permitir nicknames demasiado largos
    """
    client = ChatClient(host='localhost', port=55557)
    
    # Caso 1: Nickname vacío
    with pytest.raises(ValueError, match="El nickname no puede estar vacío"):
        client.validate_nickname("")
    
    # Caso 2: Nickname con espacios
    with pytest.raises(ValueError, match="El nickname no puede contener espacios"):
        client.validate_nickname("nombre usuario")
    
    # Caso 3: Nickname demasiado largo
    with pytest.raises(ValueError, match="El nickname es demasiado largo"):
        client.validate_nickname("estemicknameesdemasiadolargoynosepuedepermitir")
    
    # Caso 4: Nickname válido
    try:
        result = client.validate_nickname("ValidUser")
        assert result is True
    except ValueError:
        pytest.fail("Un nickname válido no debería lanzar una excepción")