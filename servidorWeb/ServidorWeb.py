import sys
import socket
import threading
import os
import datetime
import time

def filetype(file):
    # Devuelve un string con el formato del archivo
    if file.endswith(".txt"):
        return "text/plain"
    elif file.endswith(".html") or file.endswith(".htm"):
        return "text/html"
    elif file.endswith(".gif"):
        return "image/gif"
    elif file.endswith(".jpg") or file.endswith(".jpeg"):
        return "image/jpeg"
    else:
        # Formato desconocido
        return "application/octet-stream"
    
def web(newSocket, direccion):
    # Códigos respuesta
    c_200 = "HTTP/1.0 200 OK"
    c_400 = "HTTP/1.0 400 Bad Request"
    c_404 = "HTTP/1.0 404 Not Found"
    # Recibimos el mensaje y lo dividimos en los saltos de línea
    mensaje  = newSocket.recv(4096).decode("UTF-8").split("\n")
    print("Recibido mensaje: {} de: {}:{}".format(mensaje, direccion[0], direccion[1]))
    # Seleccionamos la primera línea del mensaje (línea de petición), y la dividimos en los espacios
    peticion = mensaje[0].split(" ")
    # Obtenemos la fecha actual y el server
    fecha = datetime.datetime.fromtimestamp(time.time()).strftime("%a, %d, %b, %Y %H:%M:%S %Z")
    server = "TEST"
    # Comprobamos que la longitud de la petición es correcta
    if len(peticion) != 3:
         respuesta = str(c_400 + "\nDate: " + fecha + "\nServer: " + server)
    else:
        # Asignamos cada uno de los campos de la peticion
        url = peticion[1]
        # Añadimos a la url la dirección donde se encuentra el archivo solicitado
        url = str("data" + url)
        # Comprobamos que existe el recurso solicitado
        if os.path.exists(url) == False:
            respuesta = str(c_404 + "\nDate: " + fecha + "\nServer: " + server)  
        # Comprobamos que es la url de un archivo
        elif (".") in url:
            respuesta = str(c_200 + "\nDate: " + fecha + "\nServer: " + server)
        # Como la url no contiene "." , entendemos que nos esta pidiendo un directorio
        else:
            respuesta = str(c_400 + "\nDate: " + fecha + "\nServer: " + server)
    # Enviamos la respuesta
    newSocket.send(respuesta.encode("UTF-8"))
    print("Enviada respuesta: {} a: {}:{}".format(respuesta,direccion[0], direccion[1]))
    # Nos desconectamos del cliente
    newSocket.close()
    print("Desconectado de {}:{}".format(direccion[0], direccion[1]))

def main():
    if len(sys.argv) != 2:
        print("Formato ServidorTCP <puerto>")
        sys.exit()
    try:
        # Instrucciones sockets
        # Leemos los argumentos necesarios
        puerto = int(sys.argv[1])
        # Creamos el socket orientado a conexión
        socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Asociamos el socket a cualquier dirección local en el puerto indicado
        socketServidor.bind(("", puerto))
        # Establecemos un timeout de 300 segs
        timeout = 300
        socketServidor.settimeout(timeout)
        # Ponemos el servidor en modo escucha
        print("Iniciando servidor en PUERTO: ", puerto)
        socketServidor.listen()
        print("Esperando conexión...")
        while True:
            # Nos conectamos al cliente
            newSocket, direccion = socketServidor.accept()
            print("Conectado a {}:{}".format(direccion[0], direccion[1]))
            threading.Thread(target=web, args=(newSocket, direccion)).start()     
    except socket.timeout:
        print("{} segundos sin recibir nada.".format(timeout))
    
    except:
        print("Error: {}".format(sys.exc_info()[0]))
        raise
    
    finally:
        socketServidor.close()
        
if __name__ == "__main__":
    
    main()