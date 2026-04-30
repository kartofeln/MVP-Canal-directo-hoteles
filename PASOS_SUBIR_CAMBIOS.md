# Pasos para subir los cambios y actualizar la app en LinkedIn

## 1. Abrir la terminal en la carpeta del proyecto

En Cursor/VS Code: **Terminal → Nueva terminal** (o `Ctrl+ñ`).

Luego ejecuta:

```powershell
cd c:\Workspaces\Sector_turístico_linkedin
```

---

## 2. Ver qué archivos han cambiado

```powershell
git status
```

Deberías ver `app.py` (y quizá otros) como modificados.

---

## 3. Añadir los archivos, hacer commit y subir

Copia y pega estos comandos **uno detrás de otro** (o todo el bloque):

```powershell
git add app.py
git commit -m "Ocultar DataForSEO, datos de ejemplo y límite 24h para saldo"
git push origin main
```

- Si te pide **usuario y contraseña de GitHub**: usa tu usuario y, como contraseña, un **Personal Access Token** (GitHub ya no acepta la contraseña de la cuenta). Crear token: GitHub → Settings → Developer settings → Personal access tokens → Generate new token (marca `repo`).
- Si ya tenías el repo conectado, `git push` sube los cambios a `main`.

---

## 4. Comprobar que Streamlit ha actualizado

1. Entra en **[share.streamlit.io](https://share.streamlit.io)**.
2. Abre **tu app** (la que apunta a `kartofeln/apptrends.py`).
3. Verás que está **"Building"** o **"Updating"** (suele tardar 1–2 minutos).
4. Cuando termine, abre el **enlace de la app** (ej: `https://xxx.streamlit.app`).
5. Comprueba que:
   - No se ve la barra lateral (margen derecho vacío).
   - En la pestaña "Volumen de búsqueda por destino" aparecen datos de ejemplo y el botón "Actualizar con datos en vivo".

No hace falta volver a desplegar a mano: **cada `git push` a `main` hace que Streamlit actualice la app sola**.

---

## Resumen rápido

| Paso | Comando / acción |
|------|-------------------|
| 1 | `cd c:\Workspaces\Sector_turístico_linkedin` |
| 2 | `git status` (opcional) |
| 3 | `git add app.py` |
| 4 | `git commit -m "Ocultar DataForSEO, datos de ejemplo y límite 24h"` |
| 5 | `git push origin main` |
| 6 | Esperar 1–2 min en share.streamlit.io y abrir el enlace de la app |

Si en el paso 5 te sale error de "remote" o "branch", dime el mensaje exacto y lo vemos.
