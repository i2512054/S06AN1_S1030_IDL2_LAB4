"""Prueba rápida del servicio: python main.py [ruta_xml]"""
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from services.claim_transformer import ClaimTransformerService

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_XML = BASE_DIR / "data" / "sample_claim.xml"


def main() -> int:
    xml_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_XML

    if not xml_path.exists():
        print(f"[ERROR] No se encontró el archivo: {xml_path}")
        return 1

    print(f"[INFO] Leyendo XML: {xml_path}")
    xml_content = xml_path.read_text(encoding="utf-8")

    try:
        payload = ClaimTransformerService.process_xml_to_ai_json(xml_content)
    except ValidationError as e:
        print("[ERROR] El XML no cumple el esquema de la reclamación:")
        for err in e.errors():
            campo = ".".join(str(p) for p in err["loc"])
            print(f"  - {campo}: {err['msg']}")
        return 1
    except ValueError as e:
        print(f"[ERROR] {e}")
        return 1

    print("[OK] Payload generado para IA:\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())