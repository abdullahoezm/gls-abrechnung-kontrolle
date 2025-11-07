import csv
import logging
from pathlib import Path

def run_check(config):
    log = logging.getLogger(__name__)
    input_path = Path(config["input_path"])
    output_path = Path(config["output_path"])
    toleranz = float(config.get("toleranz_euro", 0.10))

    log.info(f"Starte Prüfung: {input_path}")
    if not input_path.exists():
        log.error(f"Eingabedatei nicht gefunden: {input_path}")
        return

    with input_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=config.get("delimiter", ";"))
        rows = list(reader)

    if not rows:
        log.warning("Eingabedatei ist leer.")
        return

    expected_cols = config.get("expected_columns", [])
    missing = [c for c in expected_cols if c not in rows[0].keys()]
    if missing:
        log.error(f"Fehlende Spalten: {missing}")
        return

    # Beispielhafte Prüfung
    results = []
    for r in rows:
        try:
            betrag = float(r["betrag"])
            if abs(betrag) < toleranz:
                results.append(r)
        except ValueError:
            log.warning(f"Ungültiger Betrag in Zeile: {r}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(results)

    log.info(f"Abweichungsbericht erstellt: {output_path}")