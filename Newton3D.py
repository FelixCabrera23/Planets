#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 23:49:52 2019

@author: Félix Cabrera ECFM-USAC
asesor: Anibal Sierra

Programa que simula la gravitación segun Newton en 3Dimensiones
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import random
from time import time
import sys


"Variables importantes"
"Distancias en m x10^9"
"Masa en kg x 10 ^23"
"Fuerza en N x 10 ^28"
"Velocidad en m x 10^9 /s x 10^4 "
"Nota: un paso simulado son 10000 segundos(2.7 horas)"

G = 6.627*10**(-7) # Constante de graviatación universal
L = 800 # Limites de la grafica

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
    "Estas son planetas con masa y radio, Aunque esta vez no "
    
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
        if ref > 1200:
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
    
def Grafica (sis1):
    "Esta función grafica un sistema en R3"
    x = []
    y = []
    z = []
    for i in range(len(sis1)):
        x.append(sis1[i].x)
        y.append(sis1[i].y)
        z.append(sis1[i].z)
    
    fig = plt.figure(figsize=(8,6))
    ax1 = fig.add_subplot(111, projection = '3d')
    ax1.scatter(x,y,z, marker = 'o')
    plt.show()
    
def ran_sis (planetas,masas,vel_ran):
    """Genera un sistema con planetas aleatoreos,
        Los planetas son generados siguiendo una distribución normal
        masa aleatorea y velocidad aleatorea, si se desea.
        
        vel_ran = 0, velocidades proporcionales al radio
        vel_ran = 1, velocidades aleatoreas proporcionales al radio
        vel_ran = 2, velocidades totalmente aleatoreas.
    """
    
    sistema = [Planeta(0,0,0,0.7,19000000,0,0,0,0)]
    random.seed(1999)
    np.random.seed(1999)
    for i in range(planetas):
        ran1 = random.random()
        m1 = ran1*masas
        r1 = ran1*10**-3
        S = 60+abs(np.random.normal(0,400))
        ang1 = random.random()*2*np.pi #Angulo asimutal
        angpolar = np.random.normal()*np.pi #Angulo polar
        r = S*np.sin(angpolar)
        x1 = r*np.cos(ang1)
        y1 = r*np.sin(ang1)
        z1 = S*np.cos(angpolar)
        ang2 = -ang1 + np.pi*0.5
        if vel_ran == 0:
            vel = np.sqrt((G*19000000)/S)
            vz1 = 0
        elif vel_ran == 1:
            vel = np.sqrt((G*19000000)/S)*(np.random.normal(1.0,0.1))
            vz1 = 0
        elif vel_ran ==2:
            vel =random.random()*0.6
            vz1 =random.random()*0.07
        vx1 = -vel*np.cos(ang2)
        vy1 = vel*np.sin(ang2)
        num = i +1
        P1 = Planeta(x1,y1,z1,r1,m1,vx1,vy1,vz1,num)
        sistema.append(P1)
    return(sistema)    
    
def simul(pasos,sistema):
    """
    Esta función realiza la simulación, 
    cada paso de simulaicón corresponde a 1*10**6 segundos
    Mientras realiza la simulación guarda un arcivo con las masas y las posisiónes
    de cada uno de los planetas, cada linea es un paso de simulación
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
            file.write('%f, %f, %f, %f, ' % (m,x,y,z))
        file.write('\n')
#        Grafica(sisu)
#        Vel_graf(sisu)
#        Guardar_fig(sisu,str(i))
        for j in range(100):
            sisu = mov(sisu)
    file.close()
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

# tiempo vs numero de planetas
    
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
 