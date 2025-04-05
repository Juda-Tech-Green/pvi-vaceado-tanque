# 🚰 Simulador de Altura en Tanque Vertical

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Estado del Proyecto](https://img.shields.io/badge/Estado-En%20desarrollo-yellow)]()
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green.svg)](LICENSE)

Este proyecto simula el comportamiento del nivel de líquido en un tanque vertical con entrada y salida de fluido, resolviendo una ecuación diferencial mediante el método de Runge-Kutta de 4to orden (RK4). La interfaz gráfica está desarrollada con `Tkinter` y permite ingresar parámetros para visualizar el comportamiento dinámico del sistema.

---

## 📂 Estructura del Proyecto
```bash
├── Rk4.py # Contiene la lógica para resolver el PVI 
├── main.py # Interfaz gráfica del usuario con Tkinter 
├── README.md # Este archivo 
├── datos_realidad.csv # Datos medidos en modelo físico
├── datos_realidad_sin_per.csv # Datos medido en modelo físico con perturbaciones
├── gráficos  #Carpeta que contiene las imágenes generadas
└── valores_defect.csv (opcional) # Archivo con parámetros por defecto
```
## 📜 Licencia
MIT © [JuDa](https://github.com/Juda-Tech-Green)
Hecho con 💚 & Python

![Pro environmentalist badge](https://img.shields.io/badge/dev-environmentalist-green)