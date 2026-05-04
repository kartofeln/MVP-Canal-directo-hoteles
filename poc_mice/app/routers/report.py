from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.routers.canal_directo import summary

router = APIRouter(tags=["report"])


@router.get("/report", response_class=HTMLResponse)
def report(hotel_id: str | None = Query(default=None), db: Session = Depends(get_db)):
    data = summary(db)

    if hotel_id:
        data = [item for item in data if item.hotel.id == hotel_id]

    cards = ""

    for item in data:
        hotel = item.hotel
        run = item.latest_run

        if not run:
            continue

        score = run.score
        findings = run.findings or []

        if score >= 80:
            color = "#16a34a"
            estado = "Optimizado"
        elif score >= 60:
            color = "#f59e0b"
            estado = "Mejorable"
        else:
            color = "#dc2626"
            estado = "Riesgo alto"

        problems = ""
        if findings:
            for f in findings:
                problems += f"<li>{f.message}</li>"
        else:
            problems = "<li>No se han detectado problemas relevantes.</li>"

        cards += f"""
        <div class="card">
            <h2>{hotel.name}</h2>
            <p><strong>Dominio analizado:</strong> {hotel.official_domain}</p>
            <div class="score" style="background:{color};">{score}/100</div>
            <p><strong>Estado:</strong> {estado}</p>
            <h3>Problemas detectados</h3>
            <ul>{problems}</ul>
            <h3>Lectura comercial</h3>
            <p>Más reservas directas = recuperar el control sobre la captación del hotel.</p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Diagnóstico Canal Directo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background:#f3f4f6;
                padding:40px;
                color:#111827;
            }}
            .card {{
                max-width:850px;
                margin:0 auto 28px auto;
                background:white;
                padding:32px;
                border-radius:20px;
                box-shadow:0 10px 30px rgba(0,0,0,0.08);
            }}
            .score {{
                width:120px;
                height:120px;
                border-radius:999px;
                color:white;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:28px;
                font-weight:bold;
                margin:24px 0;
            }}
            li {{ margin-bottom:10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Diagnóstico de Canal Directo Hotelero</h1>
            <p>Informe inicial para detectar dependencia de intermediarios y oportunidades de venta directa.</p>
        </div>
        {cards}
    </body>
    </html>
    """


@router.get("/analiza", response_class=HTMLResponse)
def analiza():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Analiza tu hotel</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(rgba(15,23,42,0.82), rgba(15,23,42,0.82)),
                            url("https://images.unsplash.com/photo-1566073771259-6a8506099945");
                background-size: cover;
                background-position: center;
                min-height: 100vh;
                padding: 40px;
                color: #111827;
            }
            .card {
                max-width: 760px;
                margin: 40px auto;
                background: rgba(255,255,255,0.96);
                padding: 40px;
                border-radius: 24px;
                box-shadow: 0 25px 70px rgba(0,0,0,0.35);
            }
            .badge {
                display: inline-block;
                background: #dbeafe;
                color: #1d4ed8;
                padding: 8px 12px;
                border-radius: 999px;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 18px;
            }
            h1 {
                font-size: 38px;
                line-height: 1.1;
                margin: 0 0 16px;
            }
            .subtitle {
                font-size: 18px;
                color: #374151;
                line-height: 1.5;
                margin-bottom: 24px;
            }
            input, button {
                width: 100%;
                padding: 16px;
                margin: 8px 0;
                font-size: 16px;
                border-radius: 12px;
            }
            input { border: 1px solid #cbd5e1; }
            button {
                background: #2563eb;
                color: white;
                cursor: pointer;
                font-weight: bold;
                border: none;
            }
            button:hover { background: #1d4ed8; }
            .microcopy {
                color: #6b7280;
                font-size: 14px;
                text-align: center;
                margin-top: 10px;
            }
            .checks {
                margin-top: 28px;
                padding: 20px;
                background: #f8fafc;
                border-radius: 16px;
            }
            .checks li { margin-bottom: 8px; }
            .msg { margin-top: 18px; color: #374151; }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="badge">Análisis inicial gratuito</div>

            <h1>¿Tu hotel aparece antes que los intermediarios en Google?</h1>

            <p class="subtitle">
                Introduce la web de tu hotel y analiza en segundos si estás perdiendo
                reservas directas frente a intermediarios.
            </p>

            <input id="url" placeholder="Ej: https://www.tuhotel.com">

            <button onclick="runAnalysis()">Analizar mi venta directa</button>

            <p class="microcopy">
                Sin registro · Resultado inmediato · Análisis inicial MVP
            </p>

            <div class="checks">
                <p><strong>Qué comprobarás:</strong></p>
                <ul>
                    <li>Visibilidad de tu web oficial en Google</li>
                    <li>Si intermediarios u otras plataformas te adelantan</li>
                    <li>Oportunidades para recuperar reservas directas</li>
                </ul>
            </div>

            <div class="msg" id="msg"></div>
        </div>

        <script>
        async function runAnalysis() {
            const msg = document.getElementById("msg");
            msg.innerHTML = "Analizando...";

            const url = document.getElementById("url").value;

            let domain = url
                .replace("https://", "")
                .replace("http://", "")
                .replace("www.", "")
                .split("/")[0];

            const payload = {
                name: domain,
                city: "Sin validar",
                country_code: "ES",
                official_domain: domain,
                brand_query: domain,
                active: true
            };

            try {
                const listRes = await fetch("/v1/canal-directo/hotels");
                const hotels = await listRes.json();

                let existing = hotels.find(h => h.official_domain === domain);
                let hotelId;

                if (existing) {
                    hotelId = existing.id;
                } else {
                    const hotelRes = await fetch("/v1/canal-directo/hotels", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify(payload)
                    });

                    if (!hotelRes.ok) {
                        const errorText = await hotelRes.text();
                        msg.innerHTML = "Error creando hotel: " + errorText;
                        return;
                    }

                    const hotel = await hotelRes.json();
                    hotelId = hotel.id;
                }

                const checkRes = await fetch("/v1/canal-directo/checks/run?hotel_id=" + hotelId, {
                    method: "POST"
                });

                if (!checkRes.ok) {
                    const errorText = await checkRes.text();
                    msg.innerHTML = "Error ejecutando diagnóstico: " + errorText;
                    return;
                }

                window.location.href = "/report?hotel_id=" + hotelId;

            } catch (err) {
                console.error(err);
                msg.innerHTML = "Error: " + err.message;
            }
        }
        </script>
    </body>
    </html>
    """
