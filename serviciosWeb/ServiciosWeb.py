import requests
from bs4 import BeautifulSoup

def Web_Scrapping_tables(url, inv = False):
    """Devuelve un diccionario con los datos de la tabla de la 
    url. Se pueden intercambiar las claves y los valores con el booleano inv"""
    
    # Obtenemos el contenido de la página
    page = requests.get(url)
    # Decodificamos el contenido
    contenido = page.content.decode('UTF-8')
    # Parseamos el contenido
    data = BeautifulSoup(contenido, 'html.parser')
    
    dic = dict()
    
    # Recorremos las filas y guardamos en el diccionario los pares columnas
    for fila in data.find_all('tr'):
        par = fila.find_all('th')
        codes = par[0].text
        names = par[1].text
        # Se intecambian si se desea el diccionario inverso
        if inv:
            codes, names = names, codes
        dic[names] = codes
        
    return dic


if __name__ == "__main__":

    # Obtenemos un diccionario para los nombres de ayuntamientos y sus códigos
    concellos = Web_Scrapping_tables("https://irdgcdinfo.data.blog/ayuntamientos/")
    
    concello = ""
    
    # Pedimos al usuario que introduzca el nombre del ayuntamiento del cual quiere saber el tiempo
    while concello not in concellos:
        concello = input("Introduce el nombre de un ayuntamiento: ")
        if concello in concellos:
            c_code = concellos[concello]
            print("Su código es: ", c_code)
        else:
            print("Concello no válido")
        
    # Obtenemos el código del tiempo en el ayuntamiento introducido por el usuario
    meteo_url = "http://servizos.meteogalicia.gal/rss/predicion/jsonPredConcellos.action?idConc=" + c_code
    meteo_page = requests.get(meteo_url)
    meteo_data = meteo_page.json()
    meteo_code = str(meteo_data["predConcello"]["listaPredDiaConcello"][0]["ceo"]["manha"])
    print("Su código meteorológico es: ", meteo_code)

    
    # Obtenemos el mensaje de texto correspondiente al código de tiempo del ayuntamiento
    sky_status = Web_Scrapping_tables("https://irdgcdinfo.data.blog/codigos/", inv = True)
    sky_name = sky_status[meteo_code]
    print("El tiempo es: ", sky_name)
    