from server import ChatServer

def main():
    # Crear e iniciar el servidor
    server = ChatServer(host='localhost', port=55555)
    print("Iniciando servidor de chat...")
    server.start_server()
    print(f"Servidor escuchando en {server.host}:{server.port}")
    
    try:
        # Iniciar la recepción de conexiones
        server.receive()
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
        server.stop_server()
        print("Servidor cerrado")

if __name__ == "__main__":
    main() 