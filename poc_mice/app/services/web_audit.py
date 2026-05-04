import requests


def audit_website(domain: str):
    url = f"https://{domain}"

    try:
        res = requests.get(url, timeout=8)
        html = res.text.lower()
    except Exception:
        return {
            "status": "risk",
            "score": 20,
            "findings": [
                {
                    "severity": "critical",
                    "message": "No se ha podido acceder a la web del hotel."
                }
            ]
        }

    findings = []
    score = 100

    booking_words = [
        "reserva",
        "reservar",
        "booking engine",
        "book now",
        "motor de reservas",
        "check availability",
        "ver disponibilidad"
    ]

    if not any(word in html for word in booking_words):
        findings.append({
            "severity": "warning",
            "message": "No se detecta motor de reservas visible."
        })
        score -= 30

    event_words = [
        "evento",
        "eventos",
        "reuniones",
        "meeting",
        "meetings",
        "mice",
        "salones",
        "banquetes",
        "congresos",
        "corporativo"
    ]

    if not any(word in html for word in event_words):
        findings.append({
            "severity": "warning",
            "message": "No se detecta contenido claro para eventos, reuniones o grupos."
        })
        score -= 25

    return {
        "status": "ok" if score >= 80 else "risk",
        "score": max(score, 0),
        "findings": findings
    }
