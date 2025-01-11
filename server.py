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
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Servidor iniciado en {self.host}:{self.port}")

    def broadcast(self, message, exclude_client=None):
        for client in self.clients:
            if client != exclude_client:
                try:
                    client.send(message)
                except:
                    self.remove_client(client)

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                if not message:
                    raise Exception("Cliente desconectado")
                self.broadcast(message, client)
            except:
                self.remove_client(client)
                break

    def remove_client(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.broadcast(f"{nickname} ha salido del chat!".encode('utf-8'))
            self.nicknames.remove(nickname)
            client.close()

    def run(self):
        self.start_server()
        while True:
            try:
                client, address = self.server.accept()
                print(f"Nueva conexión desde {address}")

                client.send("NICK".encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')

                if nickname in self.nicknames:
                    client.send("ERROR: Nickname en uso".encode('utf-8'))
                    client.close()
                    continue

                self.nicknames.append(nickname)
                self.clients.append(client)

                print(f"{nickname} se unió al chat")
                client.send("Conectado al servidor!".encode('utf-8'))
                self.broadcast(f"{nickname} se unió al chat!".encode('utf-8'))

                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.daemon = True
                thread.start()
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    server = ChatServer()
    server.run()