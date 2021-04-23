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
    
    # Obtenemos la respuesta de LocationIQ
    location_url = "https://eu1.locationiq.com/v1/search.php?key=pk.07dd18b497861e0afa27efb21376adef&q="+ concello +"&format=xml"
    location_page = requests.get(location_url)
    location_contenido = location_page.content.decode('UTF-8')
    location_data = BeautifulSoup(location_contenido, 'lxml')
    
    # Obtenemos la importancia y las coordenadas de todos los lugares relacionados con el nombre del concello
    importance_list = []
    for place in location_data.find_all('place'):
        # No tenemos en cuenta aquellos lugares "tipo administrativo",
        # para evitar los nombres de provincias (tienen la importancia más alta)
        if place['type'] != "administrative":
            importance = place['importance']
            coords = (place['lat'], place['lon'])
            importance_list.append((importance, coords))
    
    # Obtenemos el las coordenadas del lugar con mayor importancia
    i = (0, (0, 0))
    for item in importance_list:
        if float(item[0]) > float(i[0]):
            i = item
    location_coords = i[1]
    print("Sus coordenadas son: ", location_coords)