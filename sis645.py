import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Datos históricos del tipo de cambio informal (2024 - 2025)
meses_historicos = [
    "Ene 2024", "Feb 2024", "Mar 2024", "Abr 2024", "May 2024", "Jun 2024",
    "Jul 2024", "Ago 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dic 2024",
    "Ene 2025", "Feb 2025"
]
tipo_cambio_historico = [7.00, 7.10, 7.50, 8.00, 8.30, 8.90, 9.20, 9.50, 9.80, 10.20, 10.60, 11.00, 11.20, 11.30]

# Convertimos los meses a valores numéricos (0, 1, 2, ..., N)
x = np.arange(len(meses_historicos))
y = np.array(tipo_cambio_historico)

# Ajustamos un modelo de regresión lineal (y = ax + b)
a, b = np.polyfit(x, y, 1)  

# Generamos una proyección de los próximos 24 meses (hasta 2026)
meses_futuros = [datetime(2025, 3, 1) + timedelta(days=30*i) for i in range(24)]
x_futuro = np.arange(len(meses_historicos), len(meses_historicos) + len(meses_futuros))
y_futuro = a * x_futuro + b  


meses_futuros_texto = [fecha.strftime("%b %Y") for fecha in meses_futuros]

# Unimos los datos históricos con los proyectados
meses_completos = meses_historicos + meses_futuros_texto
tipo_cambio_completo = np.concatenate([y, y_futuro])

# Graficamos la evolución y proyección
plt.figure(figsize=(12, 6))
plt.plot(meses_historicos, y, marker='o', linestyle='-', color='b', label="Histórico")
plt.plot(meses_futuros_texto, y_futuro, marker='o', linestyle='--', color='r', label="Proyección")
plt.axvline(x=meses_historicos[-1], color='k', linestyle='dotted', label="Inicio de proyección")
plt.xlabel("Mes")
plt.ylabel("Bolivianos por USD")
plt.title("Evolución y Proyección del Tipo de Cambio en el Mercado Informal")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.show()

# Solicitar datos al usuario
usd_guardados = float(input("Ingrese la cantidad de dólares ahorrados desde 2023: "))

print("\nMeses disponibles para conversión:")
for i, mes in enumerate(meses_completos, 1):
    print(f"{i}. {mes} - {tipo_cambio_completo[i-1]:.2f} BOB/USD")

seleccion = int(input("\nSeleccione el número del mes en que quiere cambiar sus dólares: ")) - 1

if 0 <= seleccion < len(tipo_cambio_completo):
    tipo_cambio_seleccionado = tipo_cambio_completo[seleccion]
    bolivianos = usd_guardados * tipo_cambio_seleccionado
    print(f"\nSi cambia {usd_guardados:.2f} USD en {meses_completos[seleccion]}, recibirá aproximadamente {bolivianos:.2f} BOB.")
else:
    print("Selección inválida.")