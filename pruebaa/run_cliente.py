import threading
from client import ChatClient

def receive_messages(socket):
    """Función para recibir mensajes"""
    while True:
        try:
            message = socket.recv(1024).decode('utf-8')
            print(message)
        except:
            break

def main():
    # Crear cliente
    client = ChatClient(host='localhost', port=55555)
    
    # Solicitar nickname
    while True:
        nickname = input("Ingresa tu nickname: ")
        try:
            # Intentar conectar
            socket = client.connect(nickname)
            if socket:
                break
        except ValueError as e:
            print(f"Error: {e}")
            continue
    
    # Iniciar thread para recibir mensajes
    receive_thread = threading.Thread(target=receive_messages, args=(socket,))
    receive_thread.daemon = True
    receive_thread.start()
    
    # Loop principal para enviar mensajes
    print("¡Conectado! Escribe tus mensajes (presiona Ctrl+C para salir)")
    try:
        while True:
            message = input()
            if message.lower() == 'salir':
                break
            client.send_message(message)
    except KeyboardInterrupt:
        print("\nDesconectando...")
    finally:
        socket.close()

if __name__ == "__main__":
    main()
