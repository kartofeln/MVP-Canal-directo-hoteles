# Tourism Demand Index

Dashboard interactivo de **demanda turística** y **volumen de búsqueda** por destinos y países. Construido con Streamlit.

---

## Ver la app en vivo

**[Abrir la app →](https://tu-app.streamlit.app)** *(sustituye por tu enlace de Streamlit Cloud)*

---

## Qué incluye

- **Demand Index:** índice de demanda turística y evolución mensual con gráfico.
- **Volumen de búsqueda por destino:** tabla y gráficos por keyword (turismo España, viajes a Dubai, Grecia, Tailandia, Japón, Canarias, etc.) y por país (España, Alemania, Reino Unido, Francia, Italia).
- Datos de ejemplo por defecto; opción de actualizar con datos en vivo (máx. 1 vez cada 24 h).
- Filtros por país y keyword, descarga en CSV.

---

## Cómo se usa

1. Abre el enlace de la app.
2. En **Demand Index** ves el índice y el gráfico mensual.
3. En **Volumen de búsqueda por destino** ves la tabla y los gráficos; puedes filtrar y descargar CSV.
4. Si está disponible, el botón **«Actualizar con datos en vivo»** refresca los datos (limitado a 1 vez al día).

**Limitaciones:** actualización en vivo 1 vez cada 24 h; destinos y países están fijados en esta versión.

---

## Ejecutarla en local

```bash
git clone https://github.com/kartofeln/apptrends.py.git
cd apptrends.py
pip install -r requirements.txt
streamlit run app.py
```

Para usar datos en vivo, crea `.streamlit/secrets.toml` con tus credenciales (no subas este archivo a GitHub).

---

## Tecnologías

- **Streamlit** · Interfaz
- **Pandas** · Datos
- **Requests** · API

---

Hecho por [Fernando Egido Adrián](https://www.linkedin.com/in/fernando-egido-adrian-8972355b/)
