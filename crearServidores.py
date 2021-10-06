import string
import random
import hashlib
import os
class Range:
    def __init__(self, lb, ub):
        self.lb=lb
        self.ub=ub
    def isFirst(self):
        return self.lb>self.ub
    def member(self,id):
        if self.isFirst():
            return (id >= self.lb and id< 1<<160) or (id >= 0 and id < self.ub)
        else:
            return id >= self.lb and id < self.ub

    def toStr(self):
        if self.isFirst():
            return '[' +str(self.lb)+' , 2^160) U [' + '0, '+str(self.ub) + ')'
        else:
            return '[' +str(self.lb)+' , '+str(self.ub)+')'

def randomString(size=20):
    chars= string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))

def randomName(n=30):
    s=randomString(n)
    hash_object = hashlib.sha1(s.encode())
    name=hash_object.hexdigest()
    #print("{} -> {}".format(s,name))
    nameAsNum=int(name,16)
    #print("number -> {}".format(nameAsNum))
    return nameAsNum


def crearServidores():
    servidores=[]
    if os.stat('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\segundaentrega\\servidores.txt').st_size == 0:
        #Se crean 3 servidores
        for i in range(3):
            nombreServidor=randomName()
            datosServidores = open('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\segundaentrega\\servidores.txt', 'a')
            datosServidores.write(str(nombreServidor)+'\n')
            servidores.append(nombreServidor)
        return servidores
    else:
        nombresServidores = open('C:\\Users\\Sofia\\Documents\\utp\\arquitectura\\segundaentrega\\servidores.txt', "r")
        while(True):
            linea = nombresServidores.readline()
            if linea != '':
                servidores.append(int(linea))
            if not linea:
                break
        nombresServidores.close()
        return servidores

def rangos(servidores):
        servidores.sort() #Se organiza
        #Se crean los rangos
        rangos=[]
        #print(llavesServidores)
        rangos.append(Range(servidores[-1],servidores[0]))
        for n in range(len(servidores)-1):
            #print('n: ',n)
            lb=servidores[n]
            #print('lb: ',lb)
            ub=servidores[n+1]
            #print('ub: ',ub)
            rangos.append(Range(lb,ub))

        for r in rangos:
            print(r.toStr())

        return rangos

servidores=crearServidores()
print(servidores)
rangos(servidores)
