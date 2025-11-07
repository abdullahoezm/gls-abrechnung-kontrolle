import argparse
import yaml
from .core import run_check
from .logging_setup import setup_logging

def main():
    parser = argparse.ArgumentParser(description="GLS Abrechnung Kontrolle")
    parser.add_argument("--config", default="config.yaml", help="Pfad zur Konfigurationsdatei")
    parser.add_argument("--input", help="Pfad zur Eingabedatei (CSV)")
    parser.add_argument("--output", help="Pfad zur Ausgabedatei")
    args = parser.parse_args()

    setup_logging()
    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if args.input:
        config["input_path"] = args.input
    if args.output:
        config["output_path"] = args.output

    run_check(config)

if __name__ == "__main__":
    main()