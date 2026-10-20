from pathlib import Path

PIPELINE = Path(__file__).resolve().parents[2]
RAIZ = PIPELINE.parent

RAW_MANUAL = PIPELINE / "raw_manual"
CACHE = PIPELINE / "cache"
FIXTURES = PIPELINE / "tests" / "fixtures"
REFERENCIAS = FIXTURES / "referencias.yaml"
REPORT = PIPELINE / "REPORT.md"

PUBLIC = RAIZ / "data" / "public"
PUBLIC_INDICADORES = PUBLIC / "indicators"
PUBLIC_GEO = PUBLIC / "geo"
