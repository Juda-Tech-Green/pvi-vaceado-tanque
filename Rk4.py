import numpy as np
import matplotlib.pyplot as plt
import csv
from pandas import DataFrame
from datetime import datetime
from math import sqrt


# Cargar los valores por defecto en un diccionario para después cargarlos en la interfaz
valores_defecto = {}
with open('./valores_defecto.csv', 'r') as file:
    reader = csv.reader(file)
    for fila in reader:
        valores_defecto[fila[0]] = float(fila[1])


def solve_pvi(ti,
              tf,
              dt,
              h_max,
              ho,
              Atv,
              Ao,
              Qin,
              g,
              Cm,
              t_per1,
              Qin_per,
              t_per2,
              V_per,
              guardar=False):
    """Esta es la función principal donde se toman todos los parámetros de entrada y devuelve el gráfico"""


    # Calcular el numero de iteraciones
    numero_paso = int((tf - ti) / dt)

    # Import data del modelo físico
    data_real = np.genfromtxt(fname='./datos_realidad_sin_per.csv', delimiter=',', skip_header=1)
    # Condición inicial
    h = ho

    # arreglos par almacenar resultados

    vector_tiempo = []
    vector_h = []
    perturbacion_volumen = True  # se usa para aplicar V_per solo una vez - SWITCHE
    perturbacion_caudal = True
    Qin_efectivo = Qin  # valor por defecto
    for i in range(numero_paso):
        """Bucle de Runge-Kutta 4to orden"""
        t = ti + dt * i
        vector_tiempo.append(t)
        vector_h.append(h)

        # PERTURBACIÓN 1: cambio de caudal a partir de t_per1
        if perturbacion_caudal and t >= t_per1:
            Qin_efectivo = Qin_per
            perturbacion_caudal = False
        # PERTURBACIÓN 2: añadir volumen
        if perturbacion_volumen and t >= t_per2:
            h += V_per / Atv
            perturbacion_volumen = False  # Apagar switche

        # Ecuaciones para RK4
        try:
            if h > 0.001:
                # Estimación pendientes
                k1 = (1 / Atv) * (Qin_efectivo - Ao * Cm * (sqrt(2 * g * h))) # 0.00000001
                k2 = (1 / Atv) * (Qin_efectivo - Ao * Cm * (sqrt(2 * g * (h + 0.5 * k1 * dt))))
                k3 = (1 / Atv) * (Qin_efectivo - Ao * Cm * (sqrt(2 * g * (h + 0.5 * k2 * dt))))
                k4 = (1 / Atv) * (Qin_efectivo - Ao * Cm * (sqrt(2 * g * (h + k3 * dt))))

                dhdt = (k1 + 2 * k2 + 2 * k3 + k4) / 6
                h += dhdt * dt

            #  Limitar h a h_max si se pasa
            if h > h_max:
                h = h_max

        except ValueError:
            pass

    # Generar gráfico
    plt.clf()
    #plt.figure(figsize=(10, 6))
    plt.plot(vector_tiempo, vector_h, label='Simulación modelo')
    plt.plot(data_real[:, 0], data_real[:, 1], label='Datos reales', linestyle='--', color='purple')
    plt.axhline(h_max, color='red', linestyle=':', label='Altura máxima')

    plt.legend(loc=1)
    plt.title(label='Altura del tanque a lo largo del tiempo', fontsize=14, color='black')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Altura (cm)')
    plt.grid(color='gray')
    plt.tight_layout()




    # Almacenar datos de ultima simulación
    if guardar:
        # Datos entrada de simulación
        datos_entrada = {
            'ti': ti,
            'tf': tf,
            'dt': dt,
            'h_max': h_max,
            'Atv': Atv,
            'Ao': Ao,
            'Qin': Qin_efectivo,
            'g': g,
            'Cm': Cm,
            't_per1': t_per1,
            'Qin_per': Qin_per,
            't_per2': t_per2,
            'V_per': V_per
        }
        resultados_simulacion ={
            'Tiempo (s)': vector_tiempo,
            'Altura (cm)':vector_h
        }
        # Obtener día y hora de la simulación
        fecha_simulacion = (datetime.now().strftime('%Y') + '-' +  # Año
                            datetime.now().strftime('%B') + '-' +  # Mes
                            datetime.now().strftime('%a') + '-' +  # Día
                            datetime.now().strftime('%H') + '-' +  # Hora
                            datetime.now().strftime('%M') + '-' +  # Minuto
                            datetime.now().strftime('%S'))  # Segundo
        # Ruta donde guardar archivo
        ult_archivo = f'./resultados/{fecha_simulacion}.png'

        plt.savefig(ult_archivo)
        # Guardar datos de entrada
        with open(f'./resultados/{fecha_simulacion}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Parámetro', 'Valor'])  # Encabezados
            for clave, valor in datos_entrada.items():
                writer.writerow([clave, valor])
        # Guardar resultados de simulación en csv
        resultados_DataFrame = DataFrame(resultados_simulacion)
        resultados_DataFrame.to_csv(f'./resultados/datos-{fecha_simulacion}.csv',index=False)
        # Enviar gráfico para visualización
        plt.savefig(f"./grafico_actual.png")
        plt.close()
        return f"./grafico_actual.png"
    else:
        # Enviar gráfico para visualización
        plt.savefig(f"./grafico_actual.png")
        plt.close()
        return f"./grafico_actual.png"