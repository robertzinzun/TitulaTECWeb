import requests
url='http://172.16.1.135:8000/opciones'
respuesta=requests.get(url)

if __name__=='__main__':
    opciones=respuesta.json()
    #print(respuesta.json())
    print(opciones['opciones'])

