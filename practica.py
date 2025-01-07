def validacion(mensaje):
    return True
validacion()

def red():
    assert validacion("")== False

def validacion(mensaje):
    if not mensaje.strip():
        raise ValueError("el mensaje esta vacio")
    return("mensaje enviado")


####################

clientes = []  # Simula la base de datos

def connect_client(cliente):

    def disconnect_client(cliente):



#testing para conectar al cliente
    def test_connect_client():

    #simular cliente 
        cliente = "cliente1"
    #verificamos que la lista este vacia
    #conectamos el cliente
    connect_client(cliente)
    #verificamos que el cliente ahora este en la lista
    assert len(clientes) == 1
    #limpiamos la lista para evitar afectar otras pruebas
    clientes.clear()

#testing para desconectar
def test_disconnect_client():
    cliente = "cliente1" #simulamos un cliente conectado
    connect_client(cliente)  #desconectamos el cliente
    disconnect_client(cliente)  #verificamos que el cliente ya no esta en la lista
    assert cliente not in clientes
    assert len(clientes) == 0  #intentar desconectar un cliente no conectado, lanza error
   
########################33

def funcion_validacion_mensaje(mensaje):
    return True

def red(mensaje):   
    assert funcion_validacion_mensaje(mensaje) == False

def green(mensaje):
    assert funcion_validacion_mensaje(mensaje) == True
    with pytest.raises(ValueError, match="El mensaje no esta vacio"):


    ######################
# Paso 1: Red (Escribir una prueba que falle)
def test_multiplicacion():
    assert multiplicacion(2, 3) == 6

# Paso 2: Green (Implementar el código mínimo para que la prueba pase)
def multiplicacion(a, b):
    return a * b

# Paso 3: Refactor (Mejorar el código si es necesario)
# En este caso, la función ya es simple, no necesita refactorización.