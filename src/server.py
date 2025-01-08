import socket
import threading

class ChatServer:
    def __init__(self, host='localhost', port=55555):
        self.host = host
        self.port = port
        self.server = None
        self.clients = []
        self.nicknames = []
        
    def start_server(self):
        """Inicializa y arranca el servidor"""
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen()
        except Exception as e:
            print(f"Error al iniciar el servidor: {e}")
            if self.server:
                self.server.close()
            raise
    
    def broadcast(self, message, _client=None):
        """Envía un mensaje a todos los clientes conectados"""
        for client in self.clients:
            if client != _client:
                try:
                    client.send(message)
                except:
                    self.remove_client(client)
    
    def handle_client(self, client):
        """Maneja las conexiones individuales de clientes"""
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
        """Elimina un cliente del servidor"""
        try:
            if client in self.clients:
                index = self.clients.index(client)
                self.clients.remove(client)
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f"{nickname} ha salido del chat!".encode('utf-8'))
                client.close()
        except:
            pass

    def receive(self):
        """Acepta nuevas conexiones de clientes"""
        while True:
            try:
                client, address = self.server.accept()
                print(f"Conectado con {str(address)}")
                
                client.send('NICK'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')
                
                if nickname in self.nicknames:
                    client.send('ERROR: Nickname ya en uso'.encode('utf-8'))
                    client.close()
                    continue
                
                self.nicknames.append(nickname)
                self.clients.append(client)
                
                print(f"Nickname del cliente es {nickname}!")
                self.broadcast(f"{nickname} se unió al chat!".encode('utf-8'))
                client.send('Conectado al servidor!'.encode('utf-8'))
                
                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.daemon = True
                thread.start()
            except Exception as e:
                print(f"Error en receive: {e}")
                break

    def stop_server(self):
        """Detiene el servidor y limpia las conexiones"""
        for client in self.clients[:]:
            self.remove_client(client)
        if self.server:
            self.server.close()
