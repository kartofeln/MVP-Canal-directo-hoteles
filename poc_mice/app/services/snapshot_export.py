"""CSV / Markdown sin credenciales — solo datos ya persistidos."""

import csv
import io
from typing import Sequence

from app.models import IngestionRun, KeywordSnapshot


def _sorted_snapshots(rows: Sequence[KeywordSnapshot]) -> list[KeywordSnapshot]:
    return sorted(
        rows,
        key=lambda x: (-(x.search_volume or 0), x.market_label, x.keyword),
    )


def snapshots_to_csv_bytes(run: IngestionRun, rows: Sequence[KeywordSnapshot]) -> bytes:
    fin = run.finished_at.isoformat() if run.finished_at else ""
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(
        [
            "extraction_finished_utc",
            "run_id",
            "market",
            "location_code",
            "language_code",
            "keyword",
            "search_volume_monthly_est",
            "competition",
            "cpc",
        ]
    )
    for r in _sorted_snapshots(rows):
        w.writerow(
            [
                fin,
                str(run.id),
                r.market_label,
                r.location_code,
                r.language_code,
                r.keyword,
                r.search_volume,
                r.competition,
                r.cpc,
            ]
        )
    return buf.getvalue().encode("utf-8-sig")


def snapshots_to_markdown(run: IngestionRun, rows: Sequence[KeywordSnapshot]) -> str:
    fin = run.finished_at.isoformat() if run.finished_at else "—"
    lines = [
        "# Export MICE — intención de búsqueda (estimada)",
        "",
        f"- **Run ID:** `{run.id}`",
        f"- **Extracción (UTC):** {fin}",
        "- **Nota:** volúmenes estimados (datos de keywords); no equivalen a congresos o RFP reales.",
        "",
        "| Mercado | Keyword | Volumen mensual est. | Competencia | CPC |",
        "|---|---|---|---|---|",
    ]
    for r in _sorted_snapshots(rows):
        vol = r.search_volume if r.search_volume is not None else "—"
        comp = r.competition if r.competition is not None else "—"
        cpc = r.cpc if r.cpc is not None else "—"
        lines.append(f"| {r.market_label} | {r.keyword} | {vol} | {comp} | {cpc} |")
    return "\n".join(lines) + "\n"
