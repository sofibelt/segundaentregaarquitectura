import zmq
import os
import base64
context = zmq.Context()
s= context.socket(zmq.REP)
s.bind('tcp://*:8001') #protocol://*:puerto     * significa:

def enviar(orden,nombreArchivo,key,value):
    f = open('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\segundaentrega\\'+'servidor1'+'\\'+key, 'rb')# R lee el archivo en modo binario B
    #while True:
    print('enviando...')
    archivoLeido = f.read(1024*1024)
    #    if not archivoLeido:
    #        image_64_encode = base64.encodebytes(b'0')
    #        s.send_multipart([nombreArchivo.encode(),image_64_encode])
    #        break
    image_64_encode = base64.encodebytes(archivoLeido)
    s.send_multipart([nombreArchivo.encode(),image_64_encode])
    #respuesta=s.recv_multipart()
    #print(respuesta)
    f.close()


def recibir(orden):
    #tamanoArchivo=os.path.getsize('/home/sofia/Documentos/utp/arquitectura/semana6/'+orden[2])
    #while True:
    print("recibiendo...")
    image_64_decode = base64.decodebytes(orden[3])
    #    if orden[0]!=b'0':
#            s.send_multipart(['termino'.encode()])
#            break
#        else:
    image_result = open('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\segundaentrega\\servidor1\\'+orden[2], 'ab')#Cambiar con respecto al usuario,escritura y binario
    image_result.write(image_64_decode)
    size_file = os.path.getsize('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\segundaentrega\\servidor1\\'+orden[2])
    mensaje='documento cargado'+ str(size_file)
    print('cantidad cargada: ',size_file)
    s.send_multipart([mensaje.encode()])

            #recibir nuevas partes del documento
    #m=s.recv_multipart()
    #orden=[m[0].decode("utf-8"),m[1].decode("utf-8"),m[2].decode("utf-8"),m[3]]

while True:
    print("calculando...")
    m=s.recv_multipart()
    #     [orden.encode(),nombreArchivo.encode(),llaveDelArchivo.encode(),image_64_encode]
    orden=[m[0].decode("utf-8"),m[1].decode("utf-8"),m[2].decode("utf-8"),m[3]]
    if orden[0]=='upload':
        recibir(orden)
    if orden[0]=='download' or orden[1]=='downloadlink':
        #[orden.encode(),nombreArchivo.encode(),key.encode(),value.encode()]
        enviar(orden[0],orden[1],orden[2],orden[3].decode("utf-8"))
    if orden[0]=='sharelink':
        mensaje='C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\semana6\\servidor\\'+orden[0]+'\\'+orden[2]
        s.send_multipart([mensaje.encode()])
    if orden[0]=='list':
        list = os.listdir("servidor/"+orden[0]) # dir is your directory path
        mensaje="archivos: "+ str(list)
        s.send_multipart([mensaje.encode()])
