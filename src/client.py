import socket
import threading

class ChatClient:
    def __init__(self, host='localhost', port=55555):
        self.host = host
        self.port = port
        self.socket = None
    
    def validate_nickname(self, nickname):
        """Valida el nickname del cliente"""
        if not nickname:
            raise ValueError("El nickname no puede estar vacío")
        
        if " " in nickname:
            raise ValueError("El nickname no puede contener espacios")
        
        if len(nickname) > 20:
            raise ValueError("El nickname es demasiado largo")
        
        return True

    def connect(self, nickname):
        """Conecta al servidor con un nickname"""
        try:
            self.validate_nickname(nickname)
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            # Recibir solicitud de nickname
            response = self.socket.recv(1024).decode('utf-8')
            if response != 'NICK':
                self.socket.close()
                raise ValueError("Protocolo de conexión incorrecto")
            
            # Enviar nickname
            self.socket.send(nickname.encode('utf-8'))
            
            # Recibir confirmación
            response = self.socket.recv(1024).decode('utf-8')
            if "ERROR:" in response:
                self.socket.close()
                raise ValueError(response.replace("ERROR: ", ""))
            if "Conectado al servidor!" not in response:
                self.socket.close()
                raise ValueError("Error en la conexión")
                
            return self.socket
            
        except Exception as e:
            if self.socket:
                self.socket.close()
                self.socket = None
            raise

    def send_message(self, message):
        """Envía un mensaje al servidor"""
        if not message:
            raise ValueError("El mensaje no puede estar vacío")
        
        if len(message.encode('utf-8')) > 1024:
            raise ValueError("El mensaje excede el tamaño máximo permitido")
        
        if self.socket:
            try:
                self.socket.send(message.encode('utf-8'))
                return True
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")
                return False
        return False
