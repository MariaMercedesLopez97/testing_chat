import socket
import threading

class ChatServer:
    def __init__(self, host='localhost', port=55555):
        """
        Inicializa el servidor de chat
        
        :param host: Dirección del host (por defecto 'localhost')
        :param port: Puerto para conexiones (por defecto 55555)
        """
        self.host = host
        self.port = port
        self.clients = []  # Lista de clientes conectados
        self.nicknames = []  # Lista de apodos de clientes
        
    def start_server(self):
        """
        Inicializa y arranca el servidor de chat
        
        Crea un socket, lo enlaza a la dirección y puerto especificados,
        y lo prepara para escuchar conexiones entrantes
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Servidor iniciado en {self.host}:{self.port}")
        
    def broadcast(self, message, _client=None):
        """
        Envía un mensaje a todos los clientes conectados
        
        :param message: Mensaje a transmitir
        :param _client: Cliente que envía el mensaje (opcional, para evitar reenvío)
        """
        for client in self.clients:
            if client != _client:
                try:
                    client.send(message)
                except:
                    # Si hay un error al enviar, eliminar el cliente
                    self.remove_client(client)
    
    def handle_client(self, client):
        """
        Maneja las conexiones individuales de clientes
        
        Recibe mensajes del cliente y los retransmite a otros clientes
        
        :param client: Socket del cliente
        """
        while True:
            try:
                # Recibir mensaje del cliente
                message = client.recv(1024)
                if not message:
                    # Conexión cerrada por el cliente
                    break
                
                # Retransmitir mensaje a otros clientes
                self.broadcast(message, client)
            except:
                # Manejar errores de conexión
                break
        
        # Limpiar cliente desconectado
        self.remove_client(client)
    
    def remove_client(self, client):
        """
        Elimina un cliente del servidor
        
        :param client: Socket del cliente a eliminar
        """
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            client.close()
            
            # Eliminar nickname correspondiente
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            
            # Notificar desconexión
            print(f"{nickname} se ha desconectado")
            self.broadcast(f"{nickname} ha salido del chat.".encode('utf-8'))
    
    def receive(self):
        """
        Acepta nuevas conexiones de clientes
        
        Maneja el proceso de conexión de nuevos clientes:
        - Acepta conexión entrante
        - Solicita nickname
        - Agrega cliente a la lista de clientes
        - Inicia un hilo para manejar comunicaciones del cliente
        """
        while True:
            # Aceptar nueva conexión
            client, address = self.server.accept()
            print(f"Conectado con {str(address)}")
            
            # Solicitar nickname al cliente
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            # Agregar cliente y nickname
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            # Notificar nueva conexión
            print(f"Apodo del cliente: {nickname}")
            self.broadcast(f"{nickname} se unió al chat!".encode('utf-8'))
            client.send('Conectado al servidor!'.encode('utf-8'))
            
            # Iniciar hilo para manejar comunicaciones del cliente
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


    def validate_nickname(self, nickname):
        """
        Valida el nickname del cliente
        
        :param nickname: Nickname a validar
        :return: True si el nickname es válido
        :raises ValueError: Si el nickname no cumple con los criterios
        """
        # Validar que no esté vacío
        if not nickname:
            raise ValueError("El nickname no puede estar vacío")
        
        # Validar que no contenga espacios
        if " " in nickname:
            raise ValueError("El nickname no puede contener espacios")
        
        # Validar longitud máxima
        if len(nickname) > 20:
            raise ValueError("El nickname es demasiado largo")
        
        return True

    def connect(self, nickname):
        """
        Conectar al cliente con un nickname validado
        
        :param nickname: Nickname del cliente
        :return: Conexión de socket
        """
        # Validar nickname antes de conectar
        self.validate_nickname(nickname)
        
        # Lógica de conexión existente
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            
            # Solicitar y enviar nickname
            client_socket.send(nickname.encode('utf-8'))
            return client_socket
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None


# Opcional: Agregar código para iniciar el servidor si se ejecuta directamente
if __name__ == "__main__":
    server = ChatServer()
    server.start_server()
    server.receive()