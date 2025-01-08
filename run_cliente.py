from src.client import ChatClient
import threading

def receive_messages(socket):
    """Función para recibir mensajes"""
    while True:
        try:
            message = socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Error al recibir mensajes")
            break

def main():
    try:
        # Crear cliente
        client = ChatClient(host='localhost', port=55555)
        
        # Solicitar nickname
        while True:
            nickname = input("Ingresa tu nickname: ")
            try:
                # Conectar al servidor
                connection = client.connect(nickname)
                break
            except ValueError as e:
                print(f"Error: {e}")
                continue
        
        # Iniciar hilo para recibir mensajes
        receive_thread = threading.Thread(target=receive_messages, args=(connection,))
        receive_thread.daemon = True
        receive_thread.start()
        
        # Bucle principal para enviar mensajes
        print("¡Conectado! Escribe tus mensajes (escribe 'salir' para terminar):")
        while True:
            try:
                message = input()
                if message.lower() == 'salir':
                    break
                client.send_message(message)
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")
                break
                
    except KeyboardInterrupt:
        print("\nDesconectando...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if hasattr(client, 'socket') and client.socket:
            client.socket.close()

if __name__ == "__main__":
    main()