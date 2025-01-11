import pytest
import socket
import threading
import time
from client import ChatClient
from server import ChatServer

@pytest.fixture
def server_setup():
    """Fixture para configurar el servidor de pruebas"""
    server = ChatServer(host='localhost', port=55557)
    server.start_server()
    server_thread = threading.Thread(target=server.run)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.1)
    yield server
    server.server.close()

### Pruebas TDD (Req 2) ###
def test_validate_message_empty():
    """RED: Prueba validación de mensaje vacío"""
    client = ChatClient()
    with pytest.raises(ValueError, match="El mensaje no puede estar vacío"):
        client.validate_message("")

def test_validate_message_too_long():
    """RED: Prueba validación de mensaje muy largo"""
    client = ChatClient()
    with pytest.raises(ValueError, match="El mensaje es demasiado largo"):
        client.validate_message("a" * 1025)

### Casos Positivos y Negativos (Req 5) ###
def test_nickname_validation_positive():
    """Caso positivo: nickname válido"""
    client = ChatClient()
    assert client.validate_nickname("Usuario123") is True

def test_nickname_validation_negative():
    """Casos negativos: nicknames inválidos"""
    client = ChatClient()
    invalid_cases = [
        ("", "El nickname no puede estar vacío"),
        ("a " * 11, "El nickname no puede contener espacios"),
        ("a" * 21, "El nickname es demasiado largo")
    ]
    
    for nickname, error_msg in invalid_cases:
        with pytest.raises(ValueError, match=error_msg):
            client.validate_nickname(nickname)

def test_connection_success(server_setup):
    """Caso positivo: conexión exitosa"""
    client = ChatClient(port=55557)
    assert client.connect("TestUser") is True
    client.client.close()

def test_connection_failure():
    """Caso negativo: conexión fallida"""
    client = ChatClient(port=9999)  # Puerto no utilizado
    assert client.connect("TestUser") is False

def test_send_message_success(server_setup):
    """Caso positivo: envío de mensaje exitoso"""
    client = ChatClient(port=55557)
    client.connect("TestUser")
    assert client.send_message("Hola mundo") is True
    client.client.close()

def test_send_message_failure():
    """Caso negativo: envío de mensaje fallido"""
    client = ChatClient(port=55557)
    assert client.send_message("Mensaje sin conexión") is False