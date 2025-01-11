import socket
import threading

class ChatClient:
    def __init__(self, host='localhost', port=55555):
        self.host = host
        self.port = port
        self.nickname = None
        self.client = None

    def validate_nickname(self, nickname):
        if not nickname:
            raise ValueError("El nickname no puede estar vacío")
        if len(nickname) > 20:
            raise ValueError("El nickname es demasiado largo (máx. 20 caracteres)")
        if ' ' in nickname:
            raise ValueError("El nickname no puede contener espacios")
        return True

    def validate_message(self, message):
        if not message:
            raise ValueError("El mensaje no puede estar vacío")
        if len(message.encode('utf-8')) > 1024:
            raise ValueError("El mensaje es demasiado largo")
        return True

    def connect(self, nickname):
        try:
            self.validate_nickname(nickname)
            self.nickname = nickname
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == "NICK":
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("Error! Desconectado del servidor")
                self.client.close()
                break

    def send_message(self, message):
        try:
            self.validate_message(message)
            self.client.send(f"{self.nickname}: {message}".encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            return False

    def start(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        while True:
            try:
                message = input("")
                if message.lower() == 'salir':
                    break
                self.send_message(message)
            except:
                break

        self.client.close()

if __name__ == "__main__":
    nickname = input("Elige tu nickname: ")
    client = ChatClient()
    if client.connect(nickname):
        client.start()