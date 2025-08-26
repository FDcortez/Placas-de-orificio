import numpy as np
import math
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging

# Configuración de logging
logging.basicConfig(filename="registro_beta.log", level=logging.INFO)

def calcular_Q(beta, D, C, delta_P, rho):
    A2 = (math.pi / 4) * (beta * D)**2
    return C * A2 * math.sqrt((2 * delta_P) / (rho * (1 - beta**4)))

def calcular_beta_optimo(D, C, delta_P, rho, Q_deseado, tolerancia):
    beta_optimo = None
    beta_vals = np.linspace(0.2, 0.75, 1000)
    Q_vals = []

    for beta in beta_vals:
        Q_est = calcular_Q(beta, D, C, delta_P, rho)
        Q_vals.append(Q_est)
        if abs(Q_est - Q_deseado) < tolerancia and beta_optimo is None:
            beta_optimo = beta

    return beta_optimo, beta_vals, Q_vals

def mostrar_resultado(ventana, D, C, delta_P, rho, Q_deseado, tolerancia, beta_optimo, beta_vals, Q_vals):
    for widget in ventana.winfo_children():
        if isinstance(widget, ttk.Label) or isinstance(widget, ttk.Button):
            widget.destroy()

    logging.info(f"[β cálculo] D={D}, C={C}, ΔP={delta_P}, ρ={rho}, Q={Q_deseado}, tolerancia={tolerancia}, β_optimo={beta_optimo}")

    if beta_optimo is not None:
        resultado = f"- β óptimo calculado: {beta_optimo:.4f}"
    else:
        resultado = "- ⚠ No se encontró un β que cumpla con la tolerancia especificada.\n  Puedes ajustar la tolerancia o revisar los parámetros de entrada."

    texto = f"""
Parámetros:
- Diámetro de tubería (D): {D} m
- Coeficiente de descarga (C): {C}
- Diferencial de presión (ΔP): {delta_P} Pa
- Densidad del fluido (ρ): {rho} kg/m³
- Caudal deseado (Q): {Q_deseado} m³/s
- Tolerancia: {tolerancia}

Resultado:
{resultado}
"""

    label = ttk.Label(ventana, text=texto, justify="left", font=("Arial", 10), background="#f0f0f0", foreground="#333")
    label.pack(padx=10, pady=10)

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(beta_vals, Q_vals, label="Q estimado vs β", color="blue")
    ax.axhline(Q_deseado, color="red", linestyle="--", label="Q deseado")
    if beta_optimo is not None:
        ax.axvline(beta_optimo, color="green", linestyle="--", label=f"β óptimo: {beta_optimo:.4f}")
    ax.set_xlabel("β")
    ax.set_ylabel("Caudal Q (m³/s)")
    ax.set_title("Cálculo de β óptimo")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(padx=10, pady=10)

    def recalcular_con_tolerancia_ampliada():
        nueva_tolerancia = tolerancia * 2
        beta_nuevo, beta_vals_nuevo, Q_vals_nuevo = calcular_beta_optimo(D, C, delta_P, rho, Q_deseado, nueva_tolerancia)
        mostrar_resultado(ventana, D, C, delta_P, rho, Q_deseado, nueva_tolerancia, beta_nuevo, beta_vals_nuevo, Q_vals_nuevo)

    boton_recalcular = ttk.Button(ventana, text="Recalcular con tolerancia ampliada", command=recalcular_con_tolerancia_ampliada)
    boton_recalcular.pack(pady=5)

def iniciar_calculo():
    try:
        D = float(entry_D.get())
        C = float(entry_C.get())
        delta_P = float(entry_deltaP.get())
        rho = float(entry_rho.get())
        Q_deseado = float(entry_Q.get())
        tolerancia = float(entry_tol.get())
        
        beta_optimo, beta_vals, Q_vals = calcular_beta_optimo(D, C, delta_P, rho, Q_deseado, tolerancia)
        mostrar_resultado(ventana, D, C, delta_P, rho, Q_deseado, tolerancia, beta_optimo, beta_vals, Q_vals)
        
    except ValueError:
        messagebox.showerror("Error de entrada", "Por favor ingresa valores numéricos válidos.")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de β óptimo")

# Formulario de entrada
frame = ttk.Frame(ventana)
frame.pack(padx=10, pady=10)

ttk.Label(frame, text="Diámetro D (m):").grid(row=0, column=0, sticky="e")
entry_D = ttk.Entry(frame)
entry_D.insert(0, "0.1")
entry_D.grid(row=0, column=1)

ttk.Label(frame, text="Coeficiente C:").grid(row=1, column=0, sticky="e")
entry_C = ttk.Entry(frame)
entry_C.insert(0, "0.6")
entry_C.grid(row=1, column=1)

ttk.Label(frame, text="ΔP (Pa):").grid(row=2, column=0, sticky="e")
entry_deltaP = ttk.Entry(frame)
entry_deltaP.insert(0, "5000")
entry_deltaP.grid(row=2, column=1)

ttk.Label(frame, text="Densidad ρ (kg/m³):").grid(row=3, column=0, sticky="e")
entry_rho = ttk.Entry(frame)
entry_rho.insert(0, "1000")
entry_rho.grid(row=3, column=1)

ttk.Label(frame, text="Caudal deseado Q (m³/s):").grid(row=4, column=0, sticky="e")
entry_Q = ttk.Entry(frame)
entry_Q.insert(0, "0.002")
entry_Q.grid(row=4, column=1)

ttk.Label(frame, text="Tolerancia:").grid(row=5, column=0, sticky="e")
entry_tol = ttk.Entry(frame)
entry_tol.insert(0, "1e-6")
entry_tol.grid(row=5, column=1)

boton_calcular = ttk.Button(frame, text="Calcular β óptimo", command=iniciar_calculo)
boton_calcular.grid(row=6, column=0, columnspan=2, pady=10)

ventana.mainloop()
