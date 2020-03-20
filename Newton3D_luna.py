#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 23:49:52 2019

@author: Félix Cabrera ECFM-USAC
asesor: Anibal Sierra

Programa que simula la gravitación segun Newton en 3Dimensiones
"""

import numpy as np
from time import time
import sys


"Variables importantes"
"Distancias en m x10^6"
"Masa en kg x 10 ^23"
"Tiempo en s X 10^2"

G = 0.06627 # Constante de graviatación universal

def progress(count, total, status=''):
    " Barra de progreso, ayuda a determinar el porcentaje del proceso"
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.flush()
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

class Planeta(object):
    "Estas son planetas con masa y radio"
    
    def __init__(self,x=0,y=0,z=0,r=0,m=0,vx=0,vy=0,vz=0,n=0):
        "Esto define las propiedades de cada particulas"
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.m = m
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.n = n
        
    def v(self):
        "esta es la rapidez del planeta"
        vx = self.vx
        vy = self.vy
        vz = self.vz
        v = np.sqrt(vx**2+vy**2+vz**2)
        return(v)            
               
    def __repr__(self):
        "Esto hace que al llamar la variable nos devuelva el nombre del objeto"
        return('Planeta({0.x!r},{0.y!r},{0.y!r},{0.r!r},{0.m!r})'.format(self))

def F(m1,m2):
    "Define la fuerza entre dos particulas"
    r2 = (m1.x-m2.x)**2+(m1.y-m2.y)**2+(m1.z-m2.z)**2
    F =G*(m1.m*m2.m)/r2
    return(F)

    
def Ek(Planeta):
    "Esta función define la energia cinetica de las particulas"
    Ek = 0.5*Planeta.m*Planeta.v()**2
    return(Ek)
    
def aceleracion(Planetan,sistema):
    "Esta calcula la aceleración que sufre una particula debida al resto en el sistema"
    "dentro de esta funcion se consideran las colisiones"
    "Cuando dos planetas colicionan se conserva su volumen, asumiendo la misma densidad siempre"
    "el nuevo centro del planeta es el centro de masa"
    ax = 0
    ay = 0
    az = 0
    An = 0
    i = 0
    while i < len(sistema):
        if Planetan.n == 0:
            i+=1
            continue
        if i == Planetan.n:
            i+=1
            continue
        s = np.sqrt((Planetan.x-sistema[i].x)**2+(Planetan.y-sistema[i].y)**2+(Planetan.z-sistema[i].z)**2)
        h = np.sqrt((Planetan.x-sistema[i].x)**2+(Planetan.y-sistema[i].y)**2)
        x = sistema[i].x - Planetan.x
        y = sistema[i].y - Planetan.y
        z = sistema[i].z - Planetan.z
        r = Planetan.r + sistema[i].r
        An = F(Planetan,sistema[i])/Planetan.m
        ax = ax + An*(x/h)
        ay = ay + An*(y/h)
        az = az + An*(z/s)
        if s < r:
            rn = np.cbrt(Planetan.r**3+sistema[i].r**3)
            M = Planetan.m + sistema[i].m
            vxn = (Planetan.m*Planetan.vx + sistema[i].m*sistema[i].vx)/M
            vyn = (Planetan.m*Planetan.vy + sistema[i].m*sistema[i].vy)/M
            vzn = (Planetan.m*Planetan.vz + sistema[i].m*sistema[i].vz)/M
            xn = (Planetan.m*Planetan.x + sistema[i].m*sistema[i].x)/(Planetan.m+sistema[i].m)
            yn = (Planetan.m*Planetan.y + sistema[i].m*sistema[i].y)/(Planetan.m+sistema[i].m)
            zn = (Planetan.m*Planetan.z + sistema[i].m*sistema[i].z)/(Planetan.m+sistema[i].m)
            num = Planetan.n
            Planetam = Planeta(xn,yn,zn,rn,M,vxn,vyn,vzn,num)
            sistema[num] = Planetam
            sistema.pop(i)
            j = 0
            while j < len(sistema): # ES necesario reorganizar los planetas
                sistema[j].n = j
                j += 1
        i += 1
    return([ax,ay,az])
        
def mov (sis):
    "esta funcion mueve el sistema dependiendo de las velocidades"
    acel = []
    positions = []
    vel = []
    i = 0
    j = 0
    k = 0
    while i < len(sis):
        acel.append(aceleracion(sis[i],sis))
        i += 1
    while k < len(sis):
        x= sis[k].x
        y= sis[k].y
        z= sis[k].z
        ref = abs(x)+abs(y)+abs(z)
        if ref > (10**6):
            sis.pop(k)
            while j < len(sis):
                sis[j].n = j
                j += 1
            continue
        positions.append([x,y,z])        
        vel.append([sis[k].vx,sis[k].vy,sis[k].vz])
        k+=1
        
    l = 0
    while l < len(sis):

        xn = positions[l][0] + vel[l][0] + 0.5*acel[l][0]
        yn = positions[l][1] + vel[l][1] + 0.5*acel[l][1]
        zn = positions[l][2] + vel[l][2] + 0.5*acel[l][2]
        
        sis[l].vx = vel[l][0] + acel[l][0]
        sis[l].vy = vel[l][1] + acel[l][1]
        sis[l].vz = vel[l][2] + acel[l][2]
        sis[l].x = xn
        sis[l].y = yn
        sis[l].z = zn
        l+=1
        
    return(sis)
    
def simul(pasos,sistema):
    """
    Esta función realiza la simulación, 
    cada paso de simulaicón corresponde a 1*10**6 segundos
    Mientras realiza la simulación guarda un arcivo con las masas y las posisiónes
    de cada uno de los planetas, cada linea es un paso de simulación
    Como se estan guardando todos los datos del sistema a un archivo de texto es redundante 
    realizar graficas dentro de este mismo programa por lo que se eliminaran.
    """
    
    sisu = sistema[:]
    file = open('newton3d.dat','w')
    for i in range(pasos):
        progress(i,pasos,status='working')
        for planeta in sistema:
            m = planeta.m
            x = planeta.x
            y = planeta.y
            z = planeta.z
            vx = planeta.vx
            vy = planeta.vy
            vz = planeta.vz
            file.write('%f, %f, %f, %f, %f, %f, %f, ' % (m,x,y,z,vx,vy,vz))
        file.write('\n')
        for j in range(10):
            sisu = mov(sisu)
    file.close()
    print('\n fin \n')
    return(sisu)
    
#Para caracterizar
    
def tiempo(a,N):
    "Esta función calcula el tiempo que le toma simular a años un sistema de N particulas"
    pasos = a*52
    #Generamos un sistema:
    sisN = ran_sis(N,2,1)
    t0 = time()
    sisN = simul(pasos,sisN)
    t1 = time() - t0
    
    Col = N - len(sisN) +1 
    
    print('tiempo: '+str(t1)+'s')
    print('Colisiones: '+str(Col))
    return (t1)

#"tiempo vs numero de planetas"
#    
#tiempos = []
#planetas = []
#for i in range(200):
#    N = i*10
#    t = tiempo(1,N)
#    tiempos.append(t)
#    planetas.append(N)
#
#plt.clf()
#fig, ax = plt.subplots()
#ax.plot(tiempos,planetas)
#ax.set(xlabel = 'tiempo (años)', ylabel = 'planetas')
#ax.grid()
#plt.tight_layout()
#plt.savefig('tmpvspla.jpeg',dpi = 200)
 
Sistema1 = [Planeta(0,0,0,6.371,59.7,0,0,0,0),Planeta(354.590,0,31.646,1.737,0.734,0,0.108,0,1),Planeta(1000,1000,1000,0.002,0.0000001,-0.01,-0.01,0)]

