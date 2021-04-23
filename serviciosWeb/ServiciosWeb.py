import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    
    page = requests.get("https://irdgcdinfo.data.blog/ayuntamientos/")
    contenido = page.content.decode('UTF-8')
    data = BeautifulSoup(contenido, 'html.parser')
    
    concellos = dict()
    
    for fila in data.find_all('tr'):
        par = fila.find_all('th')
        a_code = par[0].text
        a_name = par[1].text
        concellos[a_name] = a_code
        
    concello = ""
    
    while concello not in concellos:
        concello = input("Introduce el nombre de un ayuntamiento: ")
    
        if concello in concellos:
            print("Su código es: ", concellos[concello])
        
        else:
            print("Concello no válido")
        
    


