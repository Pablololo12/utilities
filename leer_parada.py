#!/usr/local/bin/python

import json # Utilidad para parsear Json
import requests # Utilidad para descargar paginas web

# Direccion web tranvia
dirTranvia = "http://www.zaragoza.es/api/recurso/urbanismo-infraestructuras/tranvia/"
dirTranviaEnd = ".json"
# Dirccion web paradas bus
dirBus = "http://www.zaragoza.es/api/recurso/urbanismo-infraestructuras/transporte-urbano/poste/tuzsa-"
dirBusEnd = ".json"

# Funcion para buscar una parada
def buscarBus(parada):
    response = requests.get(dirBus + str(parada) + dirBusEnd)
    # En caso de que no exista la parada
    if response.status_code == 400:
        return 0

    datos_Parada = json.loads(response.text)
    for i in range(len(datos_Parada['destinos'])):
        print 'Linea ' + datos_Parada['destinos'][i]['linea'] + ' Destino ' + \
                datos_Parada['destinos'][i]['destino']
        print datos_Parada['destinos'][i]['primero']
        print datos_Parada['destinos'][i]['segundo']
        print
    return 1

# Funcion para buscar una parada
def buscarTranvia(parada):
    response = requests.get(dirTranvia + str(parada) + dirTranviaEnd)
    # En caso de que no exista la parada
    if response.status_code == 400:
        return 0

    datos_Parada = json.loads(response.text)
    for i in range(len(datos_Parada['destinos'])):
        print 'Linea ' + datos_Parada['destinos'][i]['linea'] + ' Destino ' + \
                datos_Parada['destinos'][i]['destino'] + ' Minutos ' + \
                str(datos_Parada['destinos'][i]['minutos'])
    return 1


while 1==1:
    
    entrada = raw_input('Introduce num parada: ')
    # Si la entrada es 0 termina el programa
    try:
        entrada = int(entrada)
    except ValueError:
        print 'Solo numeros!!!!!'
        continue
    if entrada == 0:
        break

    error = 0
    # Si se devuelve 1 todo ha ido bien
    if buscarBus(entrada) != 1:
        error = 1
    if buscarTranvia(entrada) != 1:
        if error == 1:
            print 'no se disponen datos'
