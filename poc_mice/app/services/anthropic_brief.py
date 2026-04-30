from anthropic import Anthropic

from app.config import Settings


def build_brief_from_table(
    settings: Settings,
    table_markdown: str,
    data_as_of: str,
) -> str:
    if not settings.anthropic_api_key:
        raise ValueError("Falta ANTHROPIC_API_KEY")

    client = Anthropic(api_key=settings.anthropic_api_key)
    system = (
        "Eres analista B2B para turismo MICE. Los números son estimaciones de "
        "intención de búsqueda (no pipeline real de eventos). Sé preciso y breve."
    )
    user = f"""Datos actualizados (extracción): {data_as_of}

Tabla agregada (mercado | keyword | volumen mensual estimado | competencia | cpc):
{table_markdown}

Genera:
1) Tres insights accionables para un director comercial MICE.
2) Qué mercado priorizar esta semana y por qué.
3) Una frase de disclaimer sobre la naturaleza de los datos.

Responde en español, tono profesional, máximo 200 palabras."""

    msg = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    block = msg.content[0]
    if block.type != "text":
        return ""
    return block.text
