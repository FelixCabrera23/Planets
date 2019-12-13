#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 23:49:52 2019

@author: Félix Cabrera ECFM-USAC
asesor: Anibal Sierra

Programa que simula la gravitación segun Newton
"""

import matplotlib.pyplot as plt
import numpy as np
import random
from time import time


"Variables importantes"
"Distancias en m x10^9"
"Masa en kg x 10 ^23"
"Fuerza en N x 10 ^28"
"Velocidad en m x 10^9 /s x 10^4 "
"Nota: un paso simulado son 10000 segundos"
" en las graficas los planetas aparecen ampliados 1000 veces"
"El sol aparece ampliado 70 veces, sin embargo sus radios si estan a escala en los calculos"

G = 6.627*10**(-7) # Constante de graviatación universal
L = 800 # Limites de la grafica


class Planeta(object):
    "Estas son planetas con masa y radio"
    
    def __init__(self,x=0,y=0,r=0,m=0,vx=0,vy=0,n=0):
        "Esto define las propiedades de cada particulas"
        self.x = x
        self.y = y
        self.r = r
        self.m = m
        self.vx = vx
        self.vy = vy
        self.n = n
        
    def v(self):
        "esta es la rapidez del planeta"
        vx = self.vx
        vy = self.vy
        v = np.sqrt(vx**2+vy**2)
        return(v)
        
    def grafica(self):
        "Esto le da a cada particula su grafica"
        # Para llamarla usar Particula.grafica()
        c = circulo(self.x,self.y,self.r,self.color())
        return(c)
    
    def color(self):
        n = self.n
        if n == 0:
            color = 'y'
        if n == 1:
            color = 'm'
        if n == 2:
            color = 'g'
        if n == 3:
            color = 'b'
        if n == 4:
            color = 'r'
        if n == 5:
            color = 'c'
        if n == 6:
            color = 'g'
        if n == 7:
            color = 'b'
        if n == 8:
            color = 'm'
        if n > 8:
            color = 'k'
        
        return(color)
            
            
               
    def __repr__(self):
        "Esto hace que al llamar la variable nos devuelva el nombre del objeto"
        return('Planeta({0.x!r},{0.y!r},{0.r!r},{0.m!r})'.format(self))

def circulo(x,y,r,cl):
    "define el circulo en las coordenadas y con su radio apropiado"
    if r > 1:
        R = r
    elif r > (0.1):
        R = r*70
    else:
        R = r*500
    if R < 1:
        R = 1
    circ = plt.Circle((x,y),R,color=cl)
    return(circ)
    
def Grafica(sis):
    "Esta parte plotea"
    plt.figure(figsize=(6,6))
    ax = plt.gca(aspect = 'equal')
    for i in range(len(sis)):
        ax.add_patch(sis[i].grafica())
    ax.set(xlabel = '$L x10^{9} [m]$', ylabel = '$L x10^{9} [m]$',
           title = 'Sistema Planetario')    
#    ax.set_facecolor('k')  # Esto pone el fondo de la grafica negro
    plt.tight_layout()
    plt.axis([-L,L,-L,L])
    plt.show()
    
def Vel_graf(sis):
    "esta genera una grafica con las velocidades"
    x = []
    y = []
    V = []
    U = []
    for planet in sis:
        x.append(planet.x)
        y.append(planet.y)
        U.append(planet.vx)
        V.append(planet.vy)
    plt.figure(figsize=(6,6))
    ax = plt.gca(aspect = 'equal') # FIXME
    ax.set(xlabel = '$L x10^{9} [m]$', 
           ylabel = '$L x10^{9} [m]$',title = 'Velocidades') 
    ax.set_aspect('equal')
    ax.quiver(x,y,U,V)
    plt.tight_layout()
    plt.axis([-L,L,-L,L]) 
    plt.show()
    return
    
    
def Guardar_fig(sis,nombre):
    plt.figure(figsize=(6,6))
    ax = plt.gca(aspect = 'equal')
    ax = plt.gca()
    for i in range(len(sis)):
        ax.add_patch(sis[i].grafica())
    ax.set(xlabel = '$L x10^{9} [m]$', 
           ylabel = '$L x10^{9} [m]$',title = 'Sistema Planetario')    
    plt.tight_layout()
    plt.axis([-L,L,-L,L])
    plt.savefig('%s.jpeg' %(nombre),dpi = 100)

def F(m1,m2):
    "Define la fuerza entre dos particulas"
    r2 = (m1.x-m2.x)**2+(m1.y-m2.y)**2
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
    Fn = 0
    i = 0
    while i < len(sistema):
        if i == Planetan.n:
            i+=1
            continue
        s = np.sqrt((Planetan.x-sistema[i].x)**2+(Planetan.y-sistema[i].y)**2)
        x = sistema[i].x - Planetan.x
        y = sistema[i].y - Planetan.y
        r = Planetan.r + sistema[i].r
        Fn = F(Planetan,sistema[i])/Planetan.m
        ax = ax + Fn*(x/s)
        ay = ay + Fn*(y/s)
        if s < r:
            rn = np.cbrt(Planetan.r**3+sistema[i].r**3)
            M = Planetan.m + sistema[i].m
            vxn = (Planetan.m*Planetan.vx + sistema[i].m*sistema[i].vx)/M
            vyn = (Planetan.m*Planetan.vy + sistema[i].m*sistema[i].vy)/M
            xn = (Planetan.m*Planetan.x + sistema[i].m*sistema[i].x)/(Planetan.m+sistema[i].m)
            yn = (Planetan.m*Planetan.y + sistema[i].m*sistema[i].y)/(Planetan.m+sistema[i].m)
            num = Planetan.n
            Planetam = Planeta(xn,yn,rn,M,vxn,vyn,num)
            sistema[num] = Planetam
            sistema.pop(i)
            j = 0
            while j < len(sistema): # ES necesario reorganizar los planetas
                sistema[j].n = j
                j += 1
        i += 1
    return([ax,ay])
        
def mov (sis):
    "esta funcion mueve el sistema dependiendo de las velocidades"
    acel = []
    positions = []
    vel = []
    k = 0
    i = 0
    while i < len(sis):
        acel.append(aceleracion(sis[i],sis))
        i += 1
    while k < len(sis):
        positions.append([sis[k].x,sis[k].y])        
        vel.append([sis[k].vx,sis[k].vy])
        k+=1
        
    l = 0
    while l < len(sis):

        xn = positions[l][0] + vel[l][0] + 0.5*acel[l][0]
        yn = positions[l][1] + vel[l][1] + 0.5*acel[l][1]
        
        sis[l].vx = vel[l][0] + acel[l][0]
        sis[l].vy = vel[l][1] + acel[l][1]
        sis[l].x = xn
        sis[l].y = yn
        l+=1
        
    return(sis)
    
def ran_sis (planetas,masas,vel_ran):
    """Genera un sistema con planetas aleatoreos,
        Los planetas son generados siguiendo una distribución normal
        masa aleatorea y velocidad aleatorea, si se desea.
        
        vel_ran = 0, velocidades proporcionales al radio
        vel_ran = 1, velocidades aleatoreas proporcionales al radio
        vel_ran = 2, velocidades totalmente aleatoreas.
    """
    
    sistema = [Planeta(0,0,0.7,19000000,0,0,0)]
    random.seed(1999)
    np.random.seed(1999)
    for i in range(planetas):
        ran1 = random.random()
        m1 = ran1*masas
        r1 = ran1*10**-3
        ran2 = 60+abs(np.random.normal(0,400))
        ang = random.random()*2*np.pi
        x1 = ran2*np.cos(ang)
        y1 = ran2*np.sin(ang)
        ang2 = -ang + np.pi*0.5
        if vel_ran == 0:
            vel = np.sqrt((G*19000000)/ran2)
        elif vel_ran == 1:
            vel = np.sqrt((G*19000000)/ran2)*(np.random.normal(1.0,0.1))
        elif vel_ran ==2:
            vel =random.random()*0.6
        vx1 = -vel*np.cos(ang2)
        vy1 = vel*np.sin(ang2)
        num = i +1
        P1 = Planeta(x1,y1,r1,m1,vx1,vy1,num)
        sistema.append(P1)
    return(sistema)    
    
def simul(pasos,sistema):
    sisu = sistema[:]
    for i in range(pasos):
#        Grafica(sisu)
#        Vel_graf(sisu)
#        Guardar_fig(sisu,str(i))
        for j in range(100):
            sisu = mov(sisu)
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
    
"Algunos sistemas de ejemplo"
    
#sistema tierra sol
#L = 200
sistema0 = [Planeta(0,0,0.6957,19891000,0,0,0),
            Planeta(149.597870691,0,6.371*10**-3,59.7,0,0.2978,1)]
            
#sistema tierra, mercurio, sol
sistema1 = [Planeta(0,0,0.6957,19891000,0,0,0),
            Planeta(57.894375,0,2.439*10**-3,3.28,0,0.478725,1),
            Planeta(149.6,0,6.371*10**-3,59.7,0,0.2978,2)]
    
#Sistema hasta jupiter
#L = 2000
sistema2 = [Planeta(0,0,0.6957,19891000,0,0,0),
            Planeta(57.894375,0,2.439*10**-3,3.28,0,0.478725,1),
            Planeta(108.20893,0,6.058*10**-3,48.69,0,0.350214,2),
            Planeta(149.6,0,6.371*10**-3,59.7,0,0.2978,3),
            Planeta(-227.93664,0,3.3895*10**-3,6.4185,0,-0.24077,4), 
            Planeta(778.412026,0,0.071492,18990,0,0.130697,5), 
            Planeta(0,1426.7254,58.232*10**-3,5688,-0.096724,0,6)]  
#Sistema que demuestra interacción de 4 cuerpos
sistema3 = [Planeta(-100,-100,20,1000000,0.5,0.5,0),Planeta(100,100,20,1000000,0,0,1),
            Planeta(-100,100,20,10000000,0,0,2), Planeta(100,-100,20,10000000,0,0,3)]

#Planetas con velocidades totalmente aleatoreas    
sistema4 = ran_sis(50,100000,2)
#sistema planetario aleatoreo velocidades proporcionales al radio
sistema5 = ran_sis(10,80,0)
#Sistema planetareo con velocidades aleatoreas prporcionales al radio
sistema6 = ran_sis(40,10,1)
#Sistema de particulas orbitando el centro de masa
sistema7 = [Planeta(-400,0,50,80000000,0,0.12,0),Planeta(400,0,50,80000000,0,-0.12,1)]