import zmq #provee la comunicacion a traves de sockets (hulk)
import sys
import base64
import os
#import json
from shasum import *
from shasumtexto import *
from servidorcentral import *
context = zmq.Context()#black box!!
link=' '
tamanoArchivo=0
llave=''
new_data={}
servidores={}
for i in range(3):
    servidores[randomName()]='tcp://localhost:'+str(8000+i)

#with open('op.json') as file:
#     new_data = json.load(file) #cargo el archivo json
#file.close()

def get_key(val):
    for key, value in new_data.items():
         if val == value:
             return key


def recibir(direccion,archivo):
    while True:
        print("recibiendo...")
        m=s.recv_multipart()
        orden=[m[0].decode("utf-8"),m[1].decode("utf-8"),m[2].decode("utf-8"),m[3]]
        image_64_decode = base64.decodebytes(orden[3])
        if image_64_decode==b'0':
            break
        else:
            image_result = open(direccion+archivo, 'wb')#Cambiar con respecto al usuario,escritura y binario
            image_result.write(image_64_decode)
            size_file = os.path.getsize(direccion+archivo)
            mensaje='documento cargado'+ str(size_file)
            #print(size_file,tamanoArchivo)
            print(size_file)
            s.send_multipart([mensaje.encode()])

def enviar(username,orden,nombreArchivo,direccion,puerto):

    llavesServidores=[]
    for key in servidores:
        llavesServidores.append(key)
    llavesServidores.sort()
    rangos=[]
    #print(llavesServidores)
    for n in range(len(llavesServidores)-1):
        #print('n: ',n)
        lb=llavesServidores[n]
        #print('lb: ',lb)
        ub=llavesServidores[n+1]
        #print('ub: ',ub)
        rangos.append(Range(lb,ub))
    rangos.append(Range(llavesServidores[len(llavesServidores)-1],llavesServidores[0]))
    for r in rangos:
        print(r.toStr())

    f = open(direccion, 'rb')# R lee el archivo en modo binario B
    while True:
        archivoLeido = f.read(1024*1024)
        if not archivoLeido:
            image_64_encode = base64.encodebytes(b'0')
    #        s.send_multipart([username.encode(),orden.encode(),nombreArchivo.encode(),image_64_encode])
            break
        image_64_encode = base64.encodebytes(archivoLeido)
        llaveDelArchivo=shasumtexto(image_64_encode)
        i=1
        for r in rangos:
            if r.member(int(llaveDelArchivo,16)):
                #print('llave Del Archivo: ',llaveDelArchivo,' al rango: ',r.toStr(),' servidor: ', i)
                break
            i+=1

        #Crea un socket y lo conecta a traves del protocolo tcp con el equipo local en el puerto 8001
        s = context.socket(zmq.REQ)
        s.connect('tcp://localhost:'+str(8000+i))
        s.send_multipart([username.encode(),orden.encode(),nombreArchivo.encode(),image_64_encode])
        respuesta=s.recv_multipart()
        print(respuesta)
    f.close()
    #respuesta=s.recv_multipart()
    #print(respuesta)





username = sys.argv[1]
orden = sys.argv[2]
nombreArchivo = sys.argv[3]

if orden=='upload':
    direccion='C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana6\\'+nombreArchivo
    #llave=shasum('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana6\\'+nombreArchivo)
    #if llave in new_data:
    #    print('ya esta el archivo')
    #else:
    #    if nombreArchivo in new_data.values():
    #        new_data.pop(get_key(nombreArchivo))
    #    new_data[llave] = nombreArchivo  #agrego valores al nuevo diccionario
    #    with open('op.json','w') as file:
    #        json.dump(new_data,file)
    #    file.close()
    enviar(username,orden,nombreArchivo,direccion,8003)

else:
    if orden=='downloadlink':
        try:
            partes = nombreArchivo.split("\\")
            nombreUsuarioDueno=partes[8]
            link=partes[9]
            #tamanoArchivo=os.path.getsize(nombreArchivo)
            mensaje=' '
            print([nombreUsuarioDueno.encode(),orden.encode(),link.encode(),mensaje.encode()])
            s.send_multipart([nombreUsuarioDueno.encode(),orden.encode(),link.encode(),mensaje.encode()])
            recibir('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana6\\servidor\\'+username+'\\',link)
        except:
            print('no se ha cargado el archivo')
    if orden=='sharelink':
        mensaje=' '
        s.send_multipart([username.encode(),orden.encode(),nombreArchivo.encode(),mensaje.encode()])
        respuesta=s.recv_multipart()
        print(respuesta[0].decode("utf-8"))
    if orden=='download':
        try:
            #tamanoArchivo=os.path.getsize('/home/sofia/Documentos/utp/arquitectura/semana6/servidor/'+username+'/'+nombreArchivo)
            mensaje=' '
            s.send_multipart([username.encode(),orden.encode(),nombreArchivo.encode(),mensaje.encode()])
            recibir('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana6\\',nombreArchivo)
        except:
            print('no se ha cargado el archivo')
    if orden=='list':
        mensaje=' '
        s.send_multipart([username.encode(),orden.encode(),nombreArchivo.encode(),mensaje.encode()])
        respuesta=s.recv_multipart()
        print(respuesta[0].decode("utf-8"))
