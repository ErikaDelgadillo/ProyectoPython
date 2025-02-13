from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from datetime import datetime, timedelta
import random
import io
import base64

app = Flask(__name__)

# Función para simular la fluctuación del dólar
def simular_fluctuacion(precio_gas, reservas_internacionales, especulacion, escasez, venta_legal_dolar, inflacion, estabilidad_politica):
    precio_oficial = 6.96  # Bs/USD

    # --- Gráfico 1: Fluctuación histórica del mercado negro (2023-2023) ---
    fechas_historicas = [datetime(2023, 1, 1) + timedelta(days=30 * i) for i in range(10)]  # Hasta octubre de 2023
    fechas_historicas_str = [fecha.strftime("%b %Y") for fecha in fechas_historicas]
    tipo_cambio_historico = [7.00, 7.50, 8.00, 8.50, 9.00, 9.50, 10.00, 10.50, 11.00, 11.30]  # Datos estimados

    # --- Gráfico 2: Simulación desde enero de 2025 ---
    fechas_simulacion = [datetime(2025, 1, 1) + timedelta(days=30 * i) for i in range(12)]  # 12 meses desde enero de 2025
    fechas_simulacion_str = [fecha.strftime("%b %Y") for fecha in fechas_simulacion]

    # Simular la fluctuación del tipo de cambio informal
    tipo_cambio_informal = [11.30]  # Iniciar en 11.30 Bs/USD (último dato histórico)
    detalles_fluctuacion = []  # Almacenar detalles de las fluctuaciones
    for i in range(1, 12):
        # Calcular la variación basada en los factores
        variacion_especulacion = tipo_cambio_informal[-1] * random.uniform(-especulacion, especulacion)
        variacion_escasez = tipo_cambio_informal[-1] * random.uniform(-escasez, escasez)
        variacion_venta_legal = tipo_cambio_informal[-1] * random.uniform(-venta_legal_dolar, venta_legal_dolar)
        variacion_inflacion = tipo_cambio_informal[-1] * random.uniform(-inflacion, inflacion)
        variacion_estabilidad = tipo_cambio_informal[-1] * (1 - estabilidad_politica) * random.uniform(-0.02, 0.02)

        # Impacto del precio del gas y las reservas internacionales
        impacto_gas = tipo_cambio_informal[-1] * (precio_gas - 3.50) * 0.01  # 1% por cada USD arriba/abajo de 3.50
        impacto_reservas = tipo_cambio_informal[-1] * (5.0 - reservas_internacionales) * 0.02  # 2% por cada mil millones abajo de 5.0

        # Variación total
        variacion_total = (
            variacion_especulacion +
            variacion_escasez +
            variacion_venta_legal +
            variacion_inflacion +
            variacion_estabilidad +
            impacto_gas +
            impacto_reservas
        )

        # Aplicar la variación total
        nuevo_tipo_cambio = tipo_cambio_informal[-1] + variacion_total
        tipo_cambio_informal.append(nuevo_tipo_cambio)

        # Detalles de la fluctuación
        detalles = {
            "Mes": fechas_simulacion_str[i],
            "Especulación": variacion_especulacion,
            "Escasez": variacion_escasez,
            "Venta legal": variacion_venta_legal,
            "Inflación": variacion_inflacion,
            "Estabilidad": variacion_estabilidad,
            "Impacto gas": impacto_gas,
            "Impacto reservas": impacto_reservas,
            "Variación total": variacion_total,
        }
        detalles_fluctuacion.append(detalles)

    # Precio oficial (constante o con pequeñas variaciones)
    tipo_cambio_oficial = [precio_oficial * (1 + random.uniform(-0.005, 0.005)) for _ in range(12)]

    # Crear la figura con dos subgráficos
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Gráfico 1: Fluctuación histórica (2023-2023)
    ax1.plot(fechas_historicas_str, tipo_cambio_historico, marker='o', linestyle='-', color='g', label="Mercado negro (2023)")
    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Bolivianos por USD")
    ax1.set_title("Fluctuación del Dólar en el Mercado Negro (2023)")
    ax1.legend()
    ax1.grid(True)
    plt.setp(ax1.get_xticklabels(), rotation=45)

    # Gráfico 2: Simulación desde enero de 2025
    ax2.plot(fechas_simulacion_str, tipo_cambio_informal, marker='o', linestyle='-', color='b', label="Mercado informal (2025)")
    ax2.plot(fechas_simulacion_str, tipo_cambio_oficial, marker='o', linestyle='-', color='r', label="Precio oficial (BCB)")
    ax2.set_xlabel("Mes")
    ax2.set_ylabel("Bolivianos por USD")
    ax2.set_title("Simulación de la Fluctuación del Dólar en Bolivia (2025)")
    ax2.legend()
    ax2.grid(True)
    plt.setp(ax2.get_xticklabels(), rotation=45)

    plt.tight_layout()

    # Guardar la figura como imagen en memoria
    img = io.BytesIO()
    FigureCanvas(fig).print_png(img)
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')

    return detalles_fluctuacion, graph_url


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtener los valores del formulario
        precio_gas = float(request.form["precio_gas"])
        reservas_internacionales = float(request.form["reservas_internacionales"])
        especulacion = float(request.form["especulacion"])
        escasez = float(request.form["escasez"])
        venta_legal_dolar = float(request.form["venta_legal_dolar"])
        inflacion = float(request.form["inflacion"])
        estabilidad_politica = float(request.form["estabilidad_politica"])

        detalles_fluctuacion, graph_url = simular_fluctuacion(precio_gas, reservas_internacionales, especulacion, escasez, venta_legal_dolar, inflacion, estabilidad_politica)

        return render_template("index.html", detalles=detalles_fluctuacion, graph_url=graph_url)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
