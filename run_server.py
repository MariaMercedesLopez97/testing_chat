from src.server import ChatServer
import threading

def main():
    try:
        # Crear y iniciar el servidor
        server = ChatServer(host='localhost', port=55555)
        server.start_server()
        print("Servidor iniciado en localhost:55555")
        print("Esperando conexiones...")
        
        # Iniciar el servidor en un hilo
        server_thread = threading.Thread(target=server.receive)
        server_thread.daemon = True
        server_thread.start()
        
        # Mantener el servidor corriendo
        while True:
            try:
                command = input()
                if command.lower() == 'salir':
                    break
            except KeyboardInterrupt:
                break
            
    except KeyboardInterrupt:
        print("\nCerrando el servidor...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.stop_server()
        print("Servidor cerrado")

if __name__ == "__main__":
    main()
