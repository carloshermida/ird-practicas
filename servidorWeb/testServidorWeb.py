#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import socket
import requests
import datetime

def contentType(file):
    if file.endswith(".txt"):
        return "text/plain"
    elif file.endswith(".html") or file.endswith(".htm"):
        return "text/html"
    elif file.endswith(".gif"):
        return "image/gif"
    elif file.endswith(".jpg") or file.endswith(".jpeg"):
        return "image/jpeg"
    else:
        return "application/octet-stream"



def checkHeaders(headers, recurso):
    try:
        fichero = "data/"+recurso
        return (headers.__contains__("Server") and headers.__contains__("Date")
              and headers.get("Last-Modified") == datetime.datetime.fromtimestamp(
                      os.path.getmtime(fichero)).strftime("%a, %d %b %Y %H:%M:%S %Z")
              and headers.get("Content-Length") == str(os.path.getsize(fichero))
              and headers.get("Content-Type") )
    except:
        return False



          
def checkContent(content, recurso):
    fichero = "data/"+recurso
    try:
        with open(fichero, 'rb') as f:
            fContent = f.read()
            return fContent == content
    except:
        return False
    



def main():
    
    if len(sys.argv) != 3:
        print("Formato TestServidorWeb <maquina> <puerto>")
        sys.exit()    

    # Leemos los argumentos necesarios
    maquina = sys.argv[1]
    puerto = int(sys.argv[2])
    urlBase = "http://"+maquina+":"+str(puerto)+"/"
    
    aciertos = 0
    totalTests = 0
    
    print("\nComprobando servidor: "+urlBase+"\n=====================\n\n")

    # 1 Comprobar multithread
    test = "Multihilo"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        # Creamos el socket orientado a conexión
        socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establecemos un timeout de 300 segs
        socketCliente.settimeout(300000)
        # Iniciamos la conexión con el servidor.
        socketCliente.connect((maquina, puerto))
        # Una vez iniciada la conexión, realizamos la consulta en otro hilo.
        r = requests.get(urlBase)
        print("OK")
        aciertos = aciertos + 1
    except socket.timeout:
        print("FALLO")
    except:
        print("FALLO")
    finally:
        socketCliente.close()
        
    # 2 Peticion no soportada
    test = "Petición no soportada"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        r = requests.post(urlBase)
        if r.status_code == 400 or r.status_code == 501:
            print("OK")
            aciertos = aciertos + 1
        else:
            print("FALLO")
    except:
        print("FALLO")

    # 3 Petición incorrecta
    test = "Petición incorrecta"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        # Creamos el socket orientado a conexión
        socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establecemos un timeout de 300 segs
        socketCliente.settimeout(300000)
        # Iniciamos la conexión con el servidor.
        socketCliente.connect((maquina, puerto))
        # Realizamos una consulta mal formada.
        socketCliente.send("42 BIEN\n\n".encode())
        r = socketCliente.recv(4096)
        if r.decode("UTF-8").upper().startswith("HTTP/1.0 400 BAD REQUEST") \
			or r.decode("UTF-8").upper().startswith("HTTP/1.1 400 BAD REQUEST"):
	        print("OK")
	        aciertos = aciertos + 1
        else:
            print("FALLO")
    except socket.timeout:
        print("FALLO")
    except:
        print("FALLO")
    finally:
        socketCliente.close()

    # 4 Fichero no existente
    test = "Fichero no encontrado"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        r = requests.get(urlBase+"invent.fake")
        if r.status_code == 404:
            print("OK")
            aciertos = aciertos + 1
        else:
            print("FALLO")
    except:
        print("FALLO")

    # 5 HEAD TXT
    test = "Head TXT"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        r = requests.head(urlBase+"fichero.txt")

        if ((r.status_code == 200) and (len(r.text) == 0) 
            and checkHeaders(r.headers, "fichero.txt") ):
            print("OK")
            aciertos = aciertos + 1
        else:
            print("FALLO")
    except:
        print("FALLO")

    # 6 GET TXT
    test = "Get TXT"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        r = requests.get(urlBase+"fichero.txt")
        if (r.status_code == 200 and checkHeaders(r.headers, "fichero.txt")
            and checkContent(r.content, "fichero.txt")):
            print("OK")
            aciertos = aciertos + 1
        else:
            print("FALLO")
    except:
        print("FALLO")

    # 7 HEAD HTML
    test = "Head HTML"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        r = requests.head(urlBase+"index.html")
        if ((r.status_code == 200) and (len(r.text) == 0)
            and checkHeaders(r.headers, "index.html")):
            print("OK")
            aciertos = aciertos + 1
        else:
            print("FALLO")
    except:
        print("FALLO")
    
    # 8 GET HTML
    test = "Get HTML"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        r = requests.get(urlBase+"index.html")
        if (r.status_code == 200 and checkHeaders(r.headers, "index.html")
            and checkContent(r.content, "index.html")):
            print("OK")
            aciertos = aciertos + 1
        else:
            print("FALLO")
    except:
        print("FALLO")
    
    # 9 HEAD JPG
    test = "Head JPG"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        r = requests.head(urlBase+"frightened_socket.jpg")
        if (r.status_code == 200 and len(r.text) == 0
            and checkHeaders(r.headers, "frightened_socket.jpg")):
            print("OK")
            aciertos = aciertos + 1
        else:
            print("FALLO")
    except:
        print("FALLO")
    
    # 10 GET JPG
    test = "Get JPG"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        r = requests.get(urlBase+"frightened_socket.jpg")
        if (r.status_code == 200 and checkHeaders(r.headers, "frightened_socket.jpg")
            and checkContent(r.content, "frightened_socket.jpg")):
            print("OK")
            aciertos = aciertos + 1
        else:
            print("FALLO")
    except:
        print("FALLO")
    
    # 11 HEAD GIF
    test = "Head GIF"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        r = requests.head(urlBase+"seven_segment_display.gif")
        if (r.status_code == 200 and len(r.text) == 0
            and checkHeaders(r.headers, "seven_segment_display.gif")):
            print("OK")
            aciertos = aciertos + 1
        else:
            print("FALLO")
    except:
        print("FALLO")
    
    # 12 GET GIF
    test = "Get GIF"
    print(test + ("." * (30-len(test))) , end=" ")
    totalTests = totalTests + 1
    try:
        r = requests.get(urlBase+"seven_segment_display.gif")
        if (r.status_code == 200 and checkHeaders(r.headers, "seven_segment_display.gif")
            and checkContent(r.content, "seven_segment_display.gif")):
            print("OK")
            aciertos = aciertos + 1
        else:
            print("FALLO")
    except:
        print("FALLO")


    print("\n\nPuntuación: "+str(aciertos)+"/"+str(totalTests))



if __name__ == "__main__":
    main()
