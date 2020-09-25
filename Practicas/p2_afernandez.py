#!/usr/bin/python3
import binascii
import struct

def imprimeBuff(f):
    total=4*16+2
    buffer= f.read(total)
    f.seek(446)
    cont=0
    for i in buffer:
        tmp=format(i,'02x')
        cont=cont+1
        if(cont==16):
            cont=0
def definirTipo(tipo):
    tipo=int(tipo)
    if tipo == 1:
        res='07'
    elif tipo == 3 :
        res='82'
    elif tipo == 4 :
        res='86'
    elif tipo == 5 :
        res='a5'
    else:
        res='83'
    return res

def checkpart(f):
    poss=[450, 466, 482, 498]
    while (1):
        idpart=int(input("Introduce el Id de particion(1-4): "))
        if idpart in [1,2,3,4]:
            posicion=poss[idpart-1]
            f.seek(posicion)
            val=f.read(1)
            if val == b'\x00':
                break    
            else:
                print("Particiòn ya escrita")
        else:
            print("Particion no vàlida")
    return idpart
def getLong():
    longitud=input("Ingresa el tamaño (EX: 500K, 100M o 1G)")
    if("M" in longitud):
        mult=int(longitud[:-1])*(1024**2)
    elif("G" in longitud):
        mult=int(longitud[:-1])*(1024**3)
    else:
        mult=int(longitud[:-1])*(1024)
    mult=mult/512
    return mult

disco=input("Introduce el disco a particionar: ")
path="/dev/"
path=path+disco
default='20'
with open(path,'wb+') as f:
    particion=checkpart(f)
    pos=446+16*(particion-1) #Poscion del priemr byte de x particion
    print ("Tipos aceptados:\n 1) HPFS/NTFS/exFAT\n 2) Linux \n 3) Linux Swap \n 4) NTFS \n 5) FreeBSD");
    tipo=input("Introduce el tipo de particion(1-5): ")
    tipo=definirTipo(tipo)
    mult=getLong()
    f.seek(pos)
    values=['00', '20', '00', '00', tipo, '00', '00', '00', '00', '00', '00', '00']
    for byte in values:
        item=binascii.unhexlify(str(byte))
        f.write(item)
    mult=struct.pack('<I',int(mult))
    f.write(bytes([mult[0]]))
    f.write(bytes([mult[1]]))
    f.write(bytes([mult[2]]))
    f.write(bytes([mult[3]]))
    f.seek(510,0)
    f.write(binascii.unhexlify(str('55')))
    f.write(binascii.unhexlify(str('aa')))

print("")
f.close()
