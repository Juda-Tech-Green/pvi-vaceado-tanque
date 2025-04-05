from Rk4 import solve_pvi, valores_defecto
from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("Simulador de Altura del Tanque")

# Frame para entradas
form_frame = Frame(window, padx=10, pady=10)
form_frame.grid(row=0, column=0, sticky='n')

# Frame para gráfico
plot_canvas = Canvas(window, width=640, height=580)
plot_canvas.grid(row=0, column=1, padx=10, pady=10)

graph_img = None

def obtener_valores():
    try:
        ti = float(ti_entry.get())
        tf = float(tf_entry.get())
        dt = float(dt_entry.get())
        h_max = float(hmax_entry.get())
        Atv = float(Atv_entry.get())
        Ao = float(Ao_entry.get())
        g = float(g_entry.get())
        Qin = float(Qin_entry.get())
        Cm = float(Cm_entry.get())
        return solve_pvi(ti, tf, dt, h_max, Atv, Ao, Qin, g, Cm)
    except ValueError:
        messagebox.showerror("Error", "Verifica que todos los valores numéricos sean válidos.")

def resolver():
    global graph_img
    ult_archivo = obtener_valores()
    if ult_archivo:
        graph_img = PhotoImage(file=ult_archivo)
        plot_canvas.delete("all")  # Limpia el canvas antes de dibujar de nuevo
        plot_canvas.create_image(320, 290, image=graph_img)
        plot_canvas.image = graph_img  # Retener referencia

# Helper para añadir etiquetas y campos
def add_row(label_text, row, default_value, fg=None):
    label = Label(form_frame, text=label_text, fg=fg)
    label.grid(row=row, column=0, sticky='e', pady=2)
    entry = Entry(form_frame, fg=fg) if fg else Entry(form_frame)
    entry.insert(END, default_value)
    entry.grid(row=row, column=1, pady=2)
    return entry

# Entradas
ti_entry = add_row('Tiempo inicial (s)', 0, valores_defecto['ti'])
tf_entry = add_row('Tiempo final (s)', 1, valores_defecto['tf'])
dt_entry = add_row('Delta t (s)', 2, valores_defecto['dt'])
hmax_entry = add_row('Altura máxima (cm)', 3, valores_defecto['h_max'])
Atv_entry = add_row('Área transversal tanque (cm²)', 4, valores_defecto['Atv'])
Ao_entry = add_row('Área agujero (cm²)', 5, valores_defecto['Ao'])
g_entry = add_row('Gravedad (cm/s²)', 6, valores_defecto['g'], fg='red')
Qin_entry = add_row('Caudal de entrada (cm³/s)', 7, valores_defecto['Qin'])
Cm_entry = add_row('Coeficiente de modelación 2025', 8, valores_defecto['Cm'], fg='red')

# Botón
resolver_btn = Button(form_frame, text='Resolver', command=resolver, width=20, bg='lightblue')
resolver_btn.grid(row=9, column=0, columnspan=2, pady=10)

window.mainloop()
