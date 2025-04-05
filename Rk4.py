import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
from datetime import datetime
from math import sqrt



valores_defecto = {}
with open('./valores_defecto.csv', 'r') as file:
    reader = csv.reader(file)
    for fila in reader:
        valores_defecto[fila[0]] = float(fila[1])
def solve_pvi(ti ,
              tf ,
              dt ,
              h_max ,
              Atv ,
              Ao ,
              Qin ,
              g ,
              Cm ):
    hora_simulacion = datetime.now().strftime('%H')+datetime.now().strftime('%M')+datetime.now().strftime('%S')
    # Parámetrosde simulación [cm] [s]



    numero_paso = int((tf - ti) / dt)






    # Import real data
    data_real = np.genfromtxt(fname='./datos_realidad_sin_per.csv',delimiter=',',skip_header=1)
    # Condición inicial
    h = h_max

    # arreglos par almacenar resultados

    vector_tiempo = []
    vector_h = []

    for i in range(numero_paso):
        t = ti + dt * i
        vector_tiempo.append(t)
        vector_h.append(h)
        # Ecuaciones para RK4
        # Estimacion cuatro
        try:
            if (h>0.01):
                # Estimación pendientes
                k1 = (1 / Atv) * (Qin - Ao * Cm * (sqrt(2 * g * h)))
                k2 = (1 / Atv) * (Qin - Ao * Cm * (sqrt(2 * g * (h + 0.5 * k1 * dt))))
                k3 = (1 / Atv) * (Qin - Ao * Cm * (sqrt(2 * g * (h + 0.5 * k2 * dt))))
                k4 = (1 / Atv) * (Qin - Ao * Cm * (sqrt(2 * g * (h + k3 * dt))))
                # Pendiente ponderada
                dhdt = (k1 + (2 * k2) + (2 * k3) + k4) / 6
                # Nuevo valor de h
                h = h + dhdt * dt
            else:
                break
        except ValueError:
            pass

    plt.clf()
    plt.plot(vector_tiempo,vector_h,label='Simulación modelo')
    plt.plot(data_real[:,0],data_real[:,1],label='Datos reales',linestyle='--')
    plt.legend(loc=1)
    plt.title(label='Modelo Sin perturbaciones',fontsize=14,color='black')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Altura (cm)')
    plt.grid(color='gray')
    ult_archivo = f'./gráficos/resultado_{hora_simulacion}.png'
    plt.savefig(ult_archivo)
    return ult_archivo