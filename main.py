from Rk4 import solve_pvi, valores_defecto
from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("Simulador de Altura del Tanque")
CheckVar1 = IntVar()
graph_img = None
# Frame para entradas
form_frame = Frame(window, padx=5, pady=5)
form_frame.grid(row=0, column=0, sticky='n')

# Frame para gráfico
plot_canvas = Canvas(window, width=680, height=600)
plot_canvas.grid(row=0, column=1, padx=10, pady=10)


def reset_valores_defecto():
    """Esta función toma de nuevo los valores por defecto del archivo valores_defecto.csv"""
    ti_entry.delete(0, END)
    tf_entry.delete(0, END)
    dt_entry.delete(0, END)
    hmax_entry.delete(0, END)
    ho_entry.delete(0, END)
    Atv_entry.delete(0, END)
    Ao_entry.delete(0, END)
    g_entry.delete(0, END)
    Qin_entry.delete(0, END)
    Cm_entry.delete(0, END)
    t_per1_entry.delete(0, END)
    Qin_per_entry.delete(0, END)
    t_per2_entry.delete(0, END)
    V_per_entry.delete(0, END)
    ti_entry.insert(END, valores_defecto['ti'])
    tf_entry.insert(END, valores_defecto['tf'])
    dt_entry.insert(END, valores_defecto['dt'])
    hmax_entry.insert(END, valores_defecto['h_max'])
    ho_entry.insert(END, valores_defecto['ho'])
    Atv_entry.insert(END, valores_defecto['Atv'])
    Ao_entry.insert(END, valores_defecto['Ao'])
    g_entry.insert(END, valores_defecto['g'])
    Qin_entry.insert(END, valores_defecto['Qin'])
    Cm_entry.insert(END, valores_defecto['Cm'])
    t_per1_entry.insert(END, valores_defecto['t_per1'])
    Qin_per_entry.insert(END,valores_defecto['Qin_per'])
    t_per2_entry.insert(END,valores_defecto['t_per2'])
    V_per_entry.insert(END, valores_defecto['V_per'])


def obtener_valores():
    tipo = None
    """Esta funcion toma los valores de los campos de entrada, envía los datos al módulo Rk4.py y retorna la ruta del png del gráfico, en caso de error en el tipo de variable de entrada se devuelve un mensaje de error"""
    try:
        ti = float(ti_entry.get())
        tf = float(tf_entry.get())
        dt = float(dt_entry.get())
        h_max = float(hmax_entry.get())
        ho = float(ho_entry.get())
        Atv = float(Atv_entry.get())
        Ao = float(Ao_entry.get())
        g = float(g_entry.get())
        Qin = float(Qin_entry.get())
        Cm = float(Cm_entry.get())
        t_per1 = float(t_per1_entry.get())
        Qin_per = float(Qin_per_entry.get())
        t_per2 = float(t_per2_entry.get())
        V_per = float(V_per_entry.get())
        guardar = CheckVar1.get()
        datos = [ti, tf, dt, h_max, ho, Atv, Ao, Qin, g, Cm, t_per1, Qin_per, t_per2, V_per, guardar]
        resultado = solve_pvi(ti, tf, dt, h_max, ho, Atv, Ao, Qin, g, Cm, t_per1, Qin_per, t_per2, V_per, guardar)
        # Verificadores de valores válidos
        for i in datos:
            if i < 0 or i == None:
                messagebox.showerror("Error", "Verifique que los valores de entrada sean mayores a cero.")
                return
        if (dt > 8):
            messagebox.showwarning(title='Advertencia',
                                   message='Un valor dt mayor a 8 volverá la simulación inestable.')
        if (ti > tf):
            messagebox.showerror('Error', 'Valor de tiempo inicial mayor al tiempo final.')
            return
        if (ho > h_max):
            messagebox.showerror('Error', 'Valor de la altura inicial mayor a la altura máxima del tanque.')
            return
        if t_per1>tf or t_per2>tf:
            messagebox.showwarning('Advertencia','Tiempo de perturbaciones por fuera del tiempo final de la simulación.')
            return
        if t_per1==0 and Qin_per!=0:
            messagebox.showwarning('Advertencia','El cambio de caudal no se efectuará pues el tiempo de ingreso de este cambio es cero.')
        if t_per2==0 and V_per !=0:
            messagebox.showwarning('Advertencia','El volumen de perturbación no se efectuará pues el tiempo de ingreso de este cambio es cero.')
        return resultado
    except ValueError:
        messagebox.showerror("Error", "Verifica que todos los valores numéricos sean válidos.")


def resolver():
    """Esta funcion envia los valores al módulo Rk4.py e implanta el gráfico en la GUI"""

    global graph_img
    ult_archivo = obtener_valores()
    if ult_archivo:
        graph_img = PhotoImage(file=ult_archivo)
        plot_canvas.delete("all")  # Limpia el canvas antes de dibujar de nuevo
        plot_canvas.create_image(320, 290, image=graph_img)
        plot_canvas.image = graph_img  # Retener referencia


# Funcion para añadir etiquetas y campos
def add_row(texto_label, row, valor_defecto, fg=None):
    """Esta funcion toma un texto para el albel, un valor por defecto para la entrada, un valor para el row y un fg para el color del texto"""
    label = Label(form_frame, text=texto_label, fg=fg)
    label.grid(row=row, column=0, sticky='e', pady=2)
    entry = Entry(form_frame, fg=fg) if fg else Entry(form_frame)
    entry.insert(END, valor_defecto)
    entry.grid(row=row, column=1, pady=2)
    return entry


# Entradas
entradas_label = Label(form_frame, text='Parámetros de entrada', font=('Segoe UI', 12, 'bold'))
entradas_label.grid(row=0, column=0, columnspan=2)
ti_entry = add_row('Tiempo inicial (s)', 1, valores_defecto['ti'])
tf_entry = add_row('Tiempo final (s)', 2, valores_defecto['tf'])
dt_entry = add_row('Delta t (s)', 9, valores_defecto['dt'], fg='red')
hmax_entry = add_row('Altura máxima (cm)', 4, valores_defecto['h_max'])
ho_entry = add_row('Altura inicial (cm)', 5, valores_defecto['ho'])
Atv_entry = add_row('Área transversal tanque (cm²)', 6, valores_defecto['Atv'])
Ao_entry = add_row('Área agujero (cm²)', 7, valores_defecto['Ao'])
g_entry = add_row('Gravedad (cm/s²)', 8, valores_defecto['g'], fg='red')
Qin_entry = add_row('Caudal de entrada (cm³/s)', 3, valores_defecto['Qin'])
Cm_entry = add_row('Coeficiente de modelación 2025', 10, valores_defecto['Cm'], fg='red')

# Campo de entrada para las perturbaciones

perturbacion1_label = Label(form_frame, text='PERTURBACIÓN 1: cambio de caudal', font=('Segoe UI', 10, 'bold'))
perturbacion1_label.grid(row=11, column=0, columnspan=2)
t_per1_entry = add_row('Tiempo para cambiar el caudal (s)', 12, '0', fg='blue')
Qin_per_entry = add_row('Cambio del caudal de entrada (cm³/s)', 13, '0', fg='blue')
perturbacion2_label = Label(form_frame, text='# PERTURBACIÓN 2: añadir volumen', font=('Segoe UI', 10, 'bold'))
perturbacion2_label.grid(row=14, column=0, columnspan=2)

t_per2_entry = add_row('Tiempo para introducir volumen (s)', 15, '0', fg='blue')
V_per_entry = add_row('Volumen a introducir (cm³)', 16, '0', fg='blue')

# Botón para resolver simulación
resolver_btn = Button(form_frame, text='Resolver', command=resolver, width=20, bg='lightblue')
reset_values_btn = Button(form_frame, text='Resolver', command=resolver, width=20, bg='lightblue')
# Botón para resetear valores por defecto
reset_values_btn = Button(form_frame, text='Valores por defecto', command=reset_valores_defecto, bg='#BC544B')

reset_values_btn.grid(row=17, column=1)
resolver_btn.grid(row=17, column=0, pady=10)
# Check box para guardar imagen y simulación
guardar_simulaion = Checkbutton(form_frame, text='Guardar gráfico y datos ', variable=CheckVar1)
guardar_simulaion.grid(row=18, column=0)

# Evita que la interfaz se cierre
window.mainloop()
