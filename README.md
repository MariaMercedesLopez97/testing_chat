# Chat en Tiempo Real con Python

Este proyecto implementa un sistema de chat en tiempo real utilizando sockets en Python, con pruebas unitarias y de integración.

## Requisitos
pip install -r requirements.txt

## Estructura del Proyecto
chat_project/
├── server.py # Servidor del chat
├── client.py # Cliente del chat
├── test_server.py # Pruebas del servidor
├── test_client.py # Pruebas del cliente
└── requirements.txt # Dependencias del proyecto


## Características

- Chat en tiempo real
- Múltiples clientes simultáneos
- Validación de nicknames
- Manejo de desconexiones
- Broadcast de mensajes
- Pruebas unitarias y de integración

## Cómo Ejecutar

1. **Iniciar el Servidor**
python server.py

2. **Iniciar el Cliente**
python client.py


## Funcionalidades

### Servidor
- Manejo de múltiples conexiones
- Broadcast de mensajes
- Control de nicknames únicos
- Manejo de desconexiones abruptas

### Cliente
- Validación de nicknames
- Validación de mensajes
- Conexión/desconexión limpia
- Interfaz de línea de comandos

## Pruebas

### Ejecutar Pruebas

**Ejecutar Pruebas**
python test_server.py
python test_client.py

### Tipos de Pruebas
1. **Pruebas Unitarias**
   - Validación de nicknames
   - Validación de mensajes
   - Inicialización del servidor

2. **Pruebas de Integración**
   - Comunicación entre múltiples clientes
   - Manejo de desconexiones
   - Broadcast de mensajes

3. **Pruebas TDD**
   - Validación de mensajes vacíos
   - Validación de mensajes largos

4. **Casos Positivos y Negativos**
   - Conexiones exitosas/fallidas
   - Nicknames válidos/inválidos
   - Envío de mensajes exitoso/fallido

## Limitaciones y Validaciones

- Nicknames:
  - No pueden estar vacíos
  - Máximo 20 caracteres
  - Sin espacios
  - No pueden repetirse

- Mensajes:
  - No pueden estar vacíos
  - Máximo 1024 bytes
  - Codificación UTF-8

## Uso del Chat

1. Inicia el servidor
2. Conecta múltiples clientes
3. Ingresa un nickname único
4. Envía mensajes
5. Escribe 'salir' para desconectarte

## Manejo de Errores

- Conexión fallida
- Nickname en uso
- Mensajes inválidos
- Desconexiones abruptas

## Desarrollo y Pruebas

El proyecto sigue principios de:
- TDD (Test-Driven Development)
- Pruebas unitarias
- Pruebas de integración
- Manejo de casos límite


## Pruebas

Para ejecutar las pruebas, se puede utilizar el comando `pytest` en el directorio raíz del proyecto.
pytest


