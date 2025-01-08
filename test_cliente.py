import pytest
import socket
import threading
import time
from client import ChatClient
from server import ChatServer

@pytest.fixture
def chat_server():
    """Fixture para configurar un servidor de chat para pruebas"""
    server = ChatServer(host='localhost', port=55557)
    server.start_server()
    server_thread = threading.Thread(target=server.receive)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.1)  # Dar tiempo para que el servidor inicie
    
    yield server
    
    # Limpieza después de cada prueba
    server.stop_server()

def test_client_connection(chat_server):
    """Caso positivo: conexión exitosa"""
    client = ChatClient(host='localhost', port=55557)
    connection = client.connect('TestUser')
    assert connection is not None
    connection.close()

def test_client_connection_error():
    """Caso negativo: error de conexión"""
    client = ChatClient(host='localhost', port=9999)
    with pytest.raises(Exception):
        client.connect('TestUser')

def test_client_send_message(chat_server):
    """Prueba el envío de mensajes de un cliente"""
    client1 = ChatClient(host='localhost', port=55557)
    client2 = ChatClient(host='localhost', port=55557)
    
    conn1 = client1.connect('User1')
    conn2 = client2.connect('User2')
    
    time.sleep(0.1)  # Esperar conexiones
    
    # Enviar mensaje desde client1
    mensaje = 'Hola, este es un mensaje de prueba'
    assert client1.send_message(mensaje)
    
    # Dar tiempo para que el mensaje llegue
    time.sleep(0.1)
    
    # Recibir mensaje en client2
    received = conn2.recv(1024).decode('utf-8')
    assert mensaje in received
    
    conn1.close()
    conn2.close()

def test_mensaje_vacio(chat_server):
    """Prueba el envío de mensajes vacíos"""
    client = ChatClient(host='localhost', port=55557)
    with pytest.raises(ValueError, match="El mensaje no puede estar vacío"):
        client.send_message("")

def test_mensaje_muy_largo(chat_server):
    """Prueba el envío de mensajes demasiado largos"""
    client = ChatClient(host='localhost', port=55557)
    mensaje_largo = "a" * 2000
    with pytest.raises(ValueError, match="El mensaje excede el tamaño máximo permitido"):
        client.send_message(mensaje_largo)

def test_nickname_validation():
    """Prueba la validación de nicknames"""
    client = ChatClient(host='localhost', port=55557)
    
    # Casos inválidos
    casos_invalidos = [
        ("", "El nickname no puede estar vacío"),
        ("nombre usuario", "El nickname no puede contener espacios"),
        ("a" * 21, "El nickname es demasiado largo"),
    ]
    
    for nickname, mensaje_error in casos_invalidos:
        with pytest.raises(ValueError, match=mensaje_error):
            client.validate_nickname(nickname)
    
    # Caso válido
    assert client.validate_nickname("ValidUser") is True

def test_nickname_duplicado(chat_server):
    """Caso negativo: nickname duplicado"""
    client1 = ChatClient(host='localhost', port=55557)
    client2 = ChatClient(host='localhost', port=55557)
    
    # Conectar primer cliente
    conn1 = client1.connect('TestUser')
    assert conn1 is not None
    
    # Intentar conectar segundo cliente con mismo nickname
    with pytest.raises(ValueError, match="Nickname ya en uso"):
        client2.connect('TestUser')
    
    conn1.close()
