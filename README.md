# Sistema de Chat Cliente-Servidor

## Descripción
Sistema de chat que permite la comunicación en tiempo real entre múltiples clientes a través de un servidor centralizado. El proyecto está desarrollado en Python y utiliza sockets para la comunicación en red.

## Características
- Conexión simultánea de múltiples clientes
- Validación de nicknames únicos
- Broadcast de mensajes
- Manejo robusto de desconexiones
- Suite completa de pruebas unitarias y de integración

## Requisitos
- Python 3.7+
- pytest

## Instalación
1. Clonar el repositorio
git clone https://github.com/tu-usuario/chat-system.git
2. Entrar al directorio
cd chat-system
3. Instalar las dependencias con `pip install -r requirements.txt`
4. Ejecutar los tests con `pytest`


## Estructura del Proyecto
```
chat-system/
│
├── server.py          # Implementación del servidor
├── client.py          # Implementación del cliente
├── test_server.py     # Pruebas del servidor
└── test_cliente.py    # Pruebas del cliente
```

## Ejecución
### Iniciar el Servidor
```python
from server import ChatServer

server = ChatServer(host='localhost', port=55555)
server.start_server()
```

### Iniciar el Cliente
```python
from client import ChatClient

client = ChatClient(host='localhost', port=55555)
client.connect('nickname')
```

## Pruebas
Para ejecutar las pruebas, ejecuta el siguiente comando:
```
pytest
```
## Ejecutar pruebas específicas
```
pytest test_cliente.py
pytest test_server.py
```
## Funcionalidades Principales
### Servidor (server.py)
- Gestión de conexiones de clientes
- Broadcast de mensajes
- Manejo de desconexiones
- Validación de nicknames únicos
### Cliente (client.py)
- Conexión al servidor
- Validación de nickname
- Envío de mensajes
- Manejo de errores de conexión

## Pruebas
### Pruebas Unitarias
- Validación de nicknames
- Manejo de mensajes
- Conexiones de clientes
### Pruebas de Integración
- Comunicación entre múltiples clientes
- Desconexiones abruptas
- Pruebas de carga


## Ejemplos de Uso

### Ejemplo Básico
```python
# Servidor
from server import ChatServer
import threading

server = ChatServer()
server.start_server()
server_thread = threading.Thread(target=server.receive)
server_thread.daemon = True
server_thread.start()

# Cliente
from client import ChatClient

client = ChatClient()
connection = client.connect("Usuario1")
client.send_message("¡Hola mundo!")
```


### Validaciones
```python
# Nickname inválido
try:
    client.connect("")  # Lanzará ValueError
except ValueError as e:
    print("Error:", e)

# Mensaje muy largo
try:
    client.send_message("a" * 2000)  # Lanzará ValueError
except ValueError as e:
    print("Error:", e)
```

## Limitaciones y Validaciones
### Nicknames:
- No pueden estar vacíos
- No pueden contener espacios
- Máximo 20 caracteres
- Deben ser únicos en el servidor
### Mensajes:
- No pueden estar vacíos
- Tamaño máximo: 1024 bytes
### Manejo de Errores
- Conexiones fallidas
- Nicknames duplicados
- Desconexiones inesperadas
- Mensajes inválidos
