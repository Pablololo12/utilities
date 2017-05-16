#!/usr/local/bin/python

import json # Utilidad para parsear Json
import requests # Utilidad para descargar paginas web
import Tkinter # GUI Python

# Direccion web tranvia
dirTranvia = "http://www.zaragoza.es/api/recurso/urbanismo-infraestructuras/tranvia/"
dirTranviaEnd = ".json"
# Dirccion web paradas bus
dirBus = "http://www.zaragoza.es/api/recurso/urbanismo-infraestructuras/transporte-urbano/poste/tuzsa-"
dirBusEnd = ".json"


# Declaracion de la ventana para var global
ventana = Tkinter.Tk()
barra = 0
texto = 0

# Funcion para buscar una parada
def buscarBus(parada):
    response = requests.get(dirBus + str(parada) + dirBusEnd)
    # En caso de que no exista la parada
    if response.status_code == 400:
        return 0

    datos_Parada = json.loads(response.text)
    for i in range(len(datos_Parada['destinos'])):
        texto.insert('end', 'Linea ' + datos_Parada['destinos'][i]['linea'] + ' Destino ' + \
                datos_Parada['destinos'][i]['destino'] + '\n' +
        datos_Parada['destinos'][i]['primero'] + '\n' +
        datos_Parada['destinos'][i]['segundo'] + '\n')
        
    return 1

# Funcion para buscar una parada
def buscarTranvia(parada):
    response = requests.get(dirTranvia + str(parada) + dirTranviaEnd)
    # En caso de que no exista la parada
    if response.status_code == 400:
        return 0

    datos_Parada = json.loads(response.text)
    texto.insert('end', '\n')
    for i in range(len(datos_Parada['destinos'])):
        texto.insert('end','Linea ' + datos_Parada['destinos'][i]['linea'] + ' Destino ' + \
                datos_Parada['destinos'][i]['destino'] + ' Minutos ' + \
                str(datos_Parada['destinos'][i]['minutos']) + '\n')
    return 1

def buscar(entrada):
    try:
        entrada = int(entrada)
    except ValueError:
        print 'Solo numeros!!!!!'
        return 0
    if entrada == 0:
        return 0

    texto.delete('1.0','end')
    error = 0
    # Si se devuelve 1 todo ha ido bien
    if buscarBus(entrada) != 1:
        error = 1
    if buscarTranvia(entrada) != 1:
        if error == 1:
            texto.insert('end','No se disponen datos')

# Accion al pulsar el boton
def boton():
    buscar(barra.get())
    barra.delete(0,len(barra.get()))
# Accion al hacer enter
def enter(event):
    buscar(barra.get())
    barra.delete(0,len(barra.get()))

#-----Main------

# Declaramos espacio para introduccion numero
barra = Tkinter.Entry(ventana)
barra.bind("<Return>", enter)
barra.pack()

# Declaramos boton
boton = Tkinter.Button(ventana, text="Buscar", command = boton)
boton.pack()

# Declaramos Caja texto
texto = Tkinter.Text(ventana)
texto.pack()

ventana.mainloop()
