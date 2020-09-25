#!/usr/bin/python3
"""Abisinia Fernandez Martinez, programa que crea particiones bàsicas en Linux"""
import struct
import binascii
import os


def checkPartition(device):
    poss={'1':450, '2':466, '3':482, '4':498}
    free=[]
    for item in poss:
        device.seek(poss[item])
        byte=device.read(1)
        if byte == b'\x00':
            free.append(item)
    while (True):
        if len(free) >0:
            print("Available partition ID(s):")
            for item in free:
                print("\t"+item)
            partition=str(input("ID: "))
            if partition in free:
                position=poss[partition]
                device.seek(position)
                byte=device.read(1)
                if byte == b'\x00':
                    return partition 
                else:
                    print("Written Partition. Try another one.")
            else:
                print("No valid option. Please try it again")
        else:
            return 0 

def getType():
    tipos={'a':'83', 'b':'82', 'c':'86', 'd':'a5', 'e':'bf'}
    while(True):
        print ("Available types:\n\t a) Linux \n\t b) Linux Swap \n\t c) NTFS\n\t d) FreeBSD \n\t e) Solaris");
        tipo=str(input("Partition type: "))
        if tipo in tipos:
            break
        else:
            print("No valid option, try another one.")
    return tipos[tipo]

def getLong():
    unit={'K':1024/512,'M':1024**2/512,'G':1024**3/512}
    lon=str(input("Tamaño:"))
    key=lon[len(lon)-1:]
    while(True):
        if key in unit:
            res= int(lon[:-1])*(unit[key])
            break
        else:
            print("No valid option, try something like 500K, 200M or 1G")
    return res

disk=str(input("Disk: "))
path="/dev/"+disk
with open(path,'wb+') as device:
    p=checkPartition(device)
    if(p!=0):
        device.seek(446+16*(int(p)-1))
        tipo=getType()
        size=getLong()
        values={1:'20', 4:tipo}
        for value in range(0,12,1):
            if value in values:
                item=binascii.unhexlify(values[value])
            else:
                item=binascii.unhexlify('00')
            device.write(item)
        binario=struct.pack('<I',int(size))
        for item in binario:
            device.write(bytes([item]))
        device.seek(510)
        device.write(binascii.unhexlify(str('55')))
        device.write(binascii.unhexlify(str('aa')))
    else:
        print("Not available partitions.")
device.close()
os.system('sudo fdisk -l '+path)
