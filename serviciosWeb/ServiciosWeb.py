from gmg import plotMap
import requests
from bs4 import BeautifulSoup
import time

def Web_Scrapping_tables(url, inv = False, columna = 'th'):
    """Devuelve un diccionario con los datos de la tabla de la url. 
    Se pueden intercambiar las claves y los valores con el booleano inv.
    El argumento columna varía la etiqueta que tienen asignadas las columnas"""
    
    # Obtenemos el contenido de la página
    page = requests.get(url)
    # Decodificamos el contenido
    contenido = page.content.decode('UTF-8')
    # Parseamos el contenido
    data = BeautifulSoup(contenido, 'html.parser')
    dic = dict()
    # Recorremos las filas y guardamos en el diccionario los pares columnas
    for fila in data.find_all('tr'):
        par = fila.find_all(columna)
        code = par[0].text
        name = par[1].text
        # Se intecambian si se desea el diccionario inverso
        if inv:
            code, name = name, code
        dic[name] = code
    return dic


if __name__ == "__main__":

    # Obtenemos un diccionario para los nombres de ayuntamientos y sus códigos
    concellos = Web_Scrapping_tables("https://irdgcdinfo.data.blog/ayuntamientos/")
    
    # Obtenemos un diccionario con los nombres y códigos de los concellos de los que queremos conocer el tiempo
    dic_concellos_usuario = Web_Scrapping_tables("https://ird202123.wordpress.com/data/", columna = 'td')
    
    # Creamos una lista con los nombres de los concellos
    concellos_usuario = []
    for item in dic_concellos_usuario.keys():
        concellos_usuario.append(item)
    # Eliminamos el primer elemento, pues es la cabecera de la tabla
    concellos_usuario.pop(0)
    
    # Creamos una lista para guardar los puntos a representar
    plot_list = []
    
    # Obtenemos los datos para cada uno de los concellos de la lista
    for concello in concellos_usuario:
        print("Nombre del ayuntamiento: ", concello)
        c_code = concellos[concello]
        print("Su código es: ", c_code)
       
        # Obtenemos el código del tiempo en el ayuntamiento
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
        
        # Si no se obtiene respuesta, volvemos a intentarlo despues de 1 segundo
        while location_page.status_code != 200:
            time.sleep(1)
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
               coords = (place['lon'], place['lat'])
               importance_list.append((importance, coords))
    
        # Obtenemos el las coordenadas del lugar con mayor importancia
        i = (0, (0, 0))
        for item in importance_list:
            if float(item[0]) > float(i[0]):
                i = item
        location_coords = i[1]
        print("Sus coordenadas son: ", location_coords, "(lon, lat)")
        print("-"*50)
        
        # Añadimos todos los datos necesarios a la lista para la posterior representación
        plot_list.append((meteo_code,location_coords))
    
    # Mostramos el mapa
    print("\nDatos mapa:\n")
    plotMap(plot_list)
        
    
    
    
    
    
    