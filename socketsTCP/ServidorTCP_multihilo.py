import sys
import socket
import threading

def eco(newSocket, direccion):
    # Recibimos el mensaje
    mensaje  = newSocket.recv(4096)
    print("Recibido mensaje: {} de: {}:{}".format(mensaje.decode("UTF-8"),direccion[0], direccion[1]))
    # Enviamos el mensaje
    newSocket.send(mensaje)
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
            threading.Thread(target=eco, args=(newSocket, direccion)).start()
            
    except socket.timeout:
        print("{} segundos sin recibir nada.".format(timeout))
    
    except:
        print("Error: {}".format(sys.exc_info()[0]))
        raise
    
    finally:
        socketServidor.close()
        
if __name__ == "__main__":
    
    main()