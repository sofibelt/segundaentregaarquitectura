import zmq #provee la comunicacion a traves de sockets (hulk)
import sys
import base64
import os
from shasum import *
from shasumtexto import *
from crearServidores import *
import json
archivo={}

servidores=crearServidores()
rangos=rangos(servidores)


context = zmq.Context()#black box!!
link=' '
tamanoArchivo=0
llave=''

def recibir():
    print("recibiendo...")
    m=s.recv_multipart()
    orden=[m[0].decode("utf-8"),m[1]]
    image_64_decode = base64.decodebytes(orden[1])
    image_result = open('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\segundaentrega\\'+orden[0], 'ab')#Cambiar con respecto al usuario,escritura y binario
    image_result.write(image_64_decode)
    size_file = os.path.getsize('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\segundaentrega\\'+orden[0])
    mensaje='documento cargado'
    print(size_file)

def enviar(username,orden,nombreArchivo,direccion):
    #Crea un socket y lo conecta a traves del protocolo tcp con el equipo local en el puerto 8001
    s = context.socket(zmq.REQ)

    f = open(direccion, 'rb')# R lee el archivo en modo binario B
    while True:
        archivoLeido = f.read(1024*1024)
        if not archivoLeido:
            image_64_encode = base64.encodebytes(b'0')
            break
        image_64_encode = base64.encodebytes(archivoLeido)
        llaveDelArchivo=shasumtexto(image_64_encode)
        numDelServidor=1
        for r in rangos:
            if r.member(int(llaveDelArchivo,16)):
                print('llave Del Archivo: ',llaveDelArchivo,' al rango: ',r.toStr(),' servidor: ', numDelServidor)
                break
            numDelServidor+=1
        archivo[llaveDelArchivo]=numDelServidor
        s.connect('tcp://localhost:'+str(8000+numDelServidor))
        #                [m[0].decode("utf-8"),m[1].decode("utf-8"),m[2].decode("utf-8"),m[3]]
        s.send_multipart([orden.encode(),nombreArchivo.encode(),llaveDelArchivo.encode(),image_64_encode])
        respuesta=s.recv_multipart()
        print(respuesta)
    f.close()






username = sys.argv[1]
orden = sys.argv[2]
nombreArchivo = sys.argv[3]

if orden=='upload':
    direccion='C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\segundaentrega\\'+nombreArchivo
    enviar(username,orden,nombreArchivo,direccion)
    with open(nombreArchivo+'.json','w') as file:
        json.dump(archivo,file)
    file.close()
    print(archivo)
else:
    if orden=='download':
        #lee el archivo... lo extrae y lo mete en el diccionario archivo
        with open(nombreArchivo+'.json') as file:
            archivo = json.load(file) #cargo el archivo json
        file.close()
        s = context.socket(zmq.REQ)
        for key, value in archivo.items():
            s.connect('tcp://localhost:'+str(8000+value))
            s.send_multipart([orden.encode(),nombreArchivo.encode(),str(key).encode(),str(value).encode()])
            recibir()
    if orden=='list':
        mensaje=' '
        nombreServidorAConsultar=nombreArchivo
        s = context.socket(zmq.REQ)
        s.connect('tcp://localhost:'+str(8000+int(nombreServidorAConsultar)))
        s.send_multipart([orden.encode(),nombreServidorAConsultar.encode(),mensaje.encode(),mensaje.encode()])
        respuesta=s.recv_multipart()
        print(respuesta[0].decode("utf-8"))
