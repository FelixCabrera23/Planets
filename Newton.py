#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 23:49:52 2019

@author: walberto

Programa que simula la gravitación segun Newton
"""

import matplotlib.pyplot as plt
import numpy as np
import random


"Variables importantes"
"Distancias en m x10^9"
"Masa en kg x 10 ^23"
"Fuerza en N x 10 ^32"
"Velocidad en m x 10^9 /s "

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
            color = 'k'
        if n > 8:
            color = 'b'
        
        return(color)
            
            
               
    def __repr__(self):
        "Esto hace que al llamar la variable nos devuelva el nombre del objeto"
        return('Planeta({0.x!r},{0.y!r},{0.r!r},{0.m!r})'.format(self))

def circulo(x,y,r,cl):
    "define el circulo en las coordenadas y con su radio apropiado"
    circ = plt.Circle((x,y),r,color=cl)
    return(circ)
    
def Grafica(sis):
    "Esta parte plotea"
    plt.figure(figsize=(6,6))
    ax = plt.gca(aspect = 'equal')
    ax = plt.gca()
    for i in range(len(sis)):
        ax.add_patch(sis[i].grafica())
    ax.set(xlabel = '$L x10^{23} [m]$', ylabel = '$L x10^{23} [m]$',
           title = 'Sistema Planetario')    
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
    fig, ax = plt.subplots()
    ax.set(xlabel = '$L x10^{23} [m]$', 
           ylabel = '$L x10^{23} [m]$',title = 'Velocidades') 
    ax.set_aspect('equal')
    ax.quiver(x,y,U,V)
    plt.figure(figsize=(6,6))
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
    ax.set(xlabel = '$L x10^{23} [m]$', 
           ylabel = '$L x10^{23} [m]$',title = 'Sistema Planetario')    
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
        if s < (3*r/4):
            rn = np.sqrt(Planetan.r**2+sistema[i].r**2)
            M = Planetan.m + sistema[i].m
            vxn = (Planetan.m*Planetan.vx + sistema[i].m*sistema[i].vx)/M
            vyn = (Planetan.m*Planetan.vy + sistema[i].m*sistema[i].vy)/M
            xn = Planetan.x + ((sistema[i].x-Planetan.x)/40)
            yn = Planetan.y + ((sistema[i].y-Planetan.y)/40)
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
        masa aleatorea y velocidad aleatorea, si se desea.
        
        vel_ran = 0, velocidades proporcionales al radio
        vel_ran = 1, velocidades aleatoreas proporcionales al radio
        vel_ran = 2, velocidades totalmente aleatoreas.
    """
    
    sistema = [Planeta(0,0,50,19000000,0,0,0)]
    random.seed(1999)
    np.random.seed(1999)
    for i in range(planetas):
        ran1 = random.random()
        m1 = ran1*masas
        r1 = ran1*10
        ran2 = random.randrange(60,750)
        ang = random.random()*2*np.pi
        x1 = ran2*np.cos(ang)
        y1 = ran2*np.sin(ang)
        ang2 = -ang + np.pi*0.5
        if vel_ran == 0:
            vel = np.sqrt((G*19000000)/ran2)
        elif vel_ran == 1:
            vel = (np.sqrt((G*19000000)/ran2))*(np.random.normal(1.0,0.1))
        else:
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
        Guardar_fig(sisu,str(i))
        for j in range(100):
            sisu = mov(sisu)
    return(sisu)
    
"Algunos sistemas de ejemplo"
    
#sistema tierra sol
#L = 300
sistema0 = [Planeta(0,0,50,19000000,0,0,0),Planeta(150,0,10,59.7,0,0.3,1)]
#sistema tierra, mercurio, sol
sistema1 = [Planeta(0,0,40,19000000,0,0,0),Planeta(57,0,10,3.28,0,0.48,1), Planeta(150,0,10,59.7,0,0.3,2)]
    
sistema2 = [Planeta(0,0,30,19890000,0,0,0),Planeta(57,0,5,3.28,0,0.48,1),Planeta(108,0,5,48.6,0,0.35,2), Planeta(150,0,5,59.7,0,0.3,3)]
    
sistema3 = [Planeta(0,0,30,19890000,0,0,0),Planeta(-57,0,5,3.28,0,-0.48,1),Planeta(108,0,5,48.6,0,0.35,2), Planeta(150,0,5,59.7,0,0.3,3), Planeta(-227,0,5,6.41,0,-0.24,4)]
#Sistema hasta jupiter
#L = 2000
sistema4 = [Planeta(0,0,30,19890000,0,0,0),Planeta(-57,0,5,3.28,0,-0.48,1),Planeta(108,0,5,48.6,0,0.35,2), Planeta(150,0,5,59.7,0,0.3,3), Planeta(-227,0,5,6.41,0,-0.24,4),
            Planeta(778.4,0,10,18990,0,0.13,5)]  

sistema5 = [Planeta(-100,-100,20,1000000,0.05,0.05,0),Planeta(100,100,20,1000000,0,0,1),Planeta(-100,100,20,10000000,0,0,2),Planeta(100,-100,20,10000000,0,0,3)]

#Planetas con velocidades aleatoreas    
sistema6 = ran_sis(50,100000,2)
#sistema planetario aleatoreo
sistema7 = ran_sis(10,80,0)