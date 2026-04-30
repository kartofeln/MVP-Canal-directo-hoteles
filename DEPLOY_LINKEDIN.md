# Cómo desplegar la app en Streamlit Cloud (para LinkedIn)

## 1. Subir el proyecto a GitHub

1. Crea un repositorio en [github.com](https://github.com/new) (ej: `tourism-demand-index`).
2. En tu carpeta del proyecto, ejecuta:

```bash
cd c:\Workspaces\Sector_turístico_linkedin
git init
git add app.py requirements.txt
git commit -m "App Tourism Demand Index + DataForSEO"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

(Sustituye `TU_USUARIO` y `TU_REPO` por tu usuario de GitHub y el nombre del repo.)

---

## 2. Desplegar en Streamlit Community Cloud

1. Entra en **[share.streamlit.io](https://share.streamlit.io)** e inicia sesión con GitHub.
2. Clic en **"New app"**.
3. Elige:
   - **Repository:** tu repo (ej: `tu_usuario/tourism-demand-index`).
   - **Branch:** `main`.
   - **Main file path:** `app.py`.
4. Clic en **"Advanced settings"** y añade los secretos (para que la API funcione en la nube):

   | Key           | Value              |
   |---------------|--------------------|
   | API_LOGIN     | tu_email@ejemplo.com |
   | API_PASSWORD  | tu_api_key         |

5. Clic en **"Deploy"**. En 1–2 minutos tendrás una URL como:
   `https://tourism-demand-index-xxxx.streamlit.app`

---

## 3. Compartir en LinkedIn

- Pega el **enlace** de tu app en el post.
- Opcional: añade 1–2 **capturas de pantalla** del dashboard para que se vea el resultado sin tener que entrar.

Ejemplo de texto para el post:

> He construido un dashboard de demanda turística y volumen de búsqueda por destinos (España, Grecia, Dubai, Tailandia…). Puedes explorarlo aquí: [enlace]
> #turismo #datos #streamlit

---

## Importante

- **No subas** el archivo `.streamlit/secrets.toml` a GitHub (credenciales). Configura los secretos solo en la web de Streamlit Cloud.
- Si tu repo es **privado**, en Streamlit Cloud solo puedes tener 1 app privada gratis; para más o público, el repo puede ser público y las credenciales siguen seguras en Secrets.
