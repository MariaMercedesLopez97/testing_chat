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
        """Inicializa y arranca el servidor"""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        
    def broadcast(self, message, _client=None):
        """
        Envía un mensaje a todos los clientes conectados
        
        :param message: Mensaje a transmitir
        :param _client: Cliente que envía el mensaje (opcional)
        """
        for client in self.clients:
            if client != _client:
                try:
                    client.send(message)
                except:
                    self.remove_client(client)
    
    def handle_client(self, client):
        """
        Maneja las conexiones individuales de clientes
        
        :param client: Socket del cliente
        """
        while True:
            try:
                message = client.recv(1024)
                if not message:
                    break
                self.broadcast(message, client)
            except:
                break
        
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
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
    
    def receive(self):
        """
        Acepta nuevas conexiones de clientes
        """
        while True:
            client, address = self.server.accept()
            print(f"Conectado con {str(address)}")
            
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f"Apodo del cliente: {nickname}")
            self.broadcast(f"{nickname} se unió al chat!".encode('utf-8'))
            client.send('Conectado al servidor!'.encode('utf-8'))
            
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()