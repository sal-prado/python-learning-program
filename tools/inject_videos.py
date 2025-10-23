from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception:
    print("ERROR: PyYAML no está instalado. Ejecuta:\n  python -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)


INDEX_PATH = Path("resources/videos.yml")
CALENDAR_PATH = Path("Calendario.md")


def load_index(path: Path) -> Dict[str, Any]:
    if not path.exists():
        sys.exit(f"ERROR: No existe el índice {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def videos_for_week(index: Dict[str, Any], week: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for items in (index.get("collections") or {}).values():
        for item in items:
            if week in (item.get("weeks") or []):
                out.append(item)
    # orden alfabético por título
    out.sort(key=lambda d: d.get("title", "").lower())
    return out


def build_md_section(week: str, items: List[Dict[str, Any]]) -> str:
    lines = [f"### Videos base — {week}", ""]
    if not items:
        lines.append("_(No se encontraron videos para esta semana en resources/videos.yml)_")
        return "\n".join(lines) + "\n"
    for v in items:
        title = v.get("title", "Sin título")
        url = v.get("url", "#")
        topics = ", ".join(v.get("topics", []))
        ts = v.get("timestamps") or {}
        ts_inline = ""
        if isinstance(ts, dict) and ts:
            ts_inline = " · " + ", ".join(f"{k}: {val}" for k, val in ts.items())
        lines.append(f"- [{title}]({url}) — temas: {topics}{ts_inline}")
    lines.append("")
    return "\n".join(lines) + "\n"


def inject_into_calendar(week: str, section_md: str, calendar_path: Path, create_if_missing: bool) -> None:
    if not calendar_path.exists():
        if not create_if_missing:
            sys.exit(f"ERROR: No existe {calendar_path}. Crea el archivo primero.")
        calendar_path.write_text(f"# Calendario del Programa\n\n", encoding="utf-8")

    original = calendar_path.read_text(encoding="utf-8")

    # marcadores
    start_marker = f"<!-- VIDEOS_BASE:{week} START -->"
    end_marker = f"<!-- VIDEOS_BASE:{week} END -->"

    # bloque a inyectar (con marcadores)
    block = f"{start_marker}\n{section_md}{end_marker}\n"

    # 1) Si ya hay marcadores para esa semana, reemplazar lo de adentro
    pattern = re.compile(
        rf"(?s){re.escape(start_marker)}.*?{re.escape(end_marker)}"
    )
    if pattern.search(original):
        updated = pattern.sub(block.strip() + "\n", original)
        if updated != original:
            _backup(calendar_path)
            calendar_path.write_text(updated, encoding="utf-8")
            print(f"OK: Reemplazado bloque existente {week}")
            return

    # 2) Si no hay marcadores, intentar insertar debajo del encabezado de la semana
    #    Encabezados válidos tipo: "### S11 — Decoradores..." o "### S11"
    header_re = re.compile(rf"^###\s*{re.escape(week)}\b.*$", re.MULTILINE)
    m = header_re.search(original)
    if m:
        insert_pos = m.end()
        updated = original[:insert_pos] + "\n\n" + block + original[insert_pos:]
        _backup(calendar_path)
        calendar_path.write_text(updated, encoding="utf-8")
        print(f"OK: Insertado bloque bajo encabezado {week}")
        return

    # 3) Si no se encontró encabezado de la semana, añadir al final
    updated = original.rstrip() + f"\n\n## {week}\n\n{block}"
    _backup(calendar_path)
    calendar_path.write_text(updated, encoding="utf-8")
    print(f"OK: Añadido bloque {week} al final (no se encontró encabezado).")


def _backup(path: Path) -> None:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak-{ts}")
    backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    # Solo informativo:
    print(f"(Backup creado: {backup.name})")


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Inyecta la sección 'Videos base' en Calendario.md usando resources/videos.yml."
    )
    ap.add_argument("-w", "--week", required=True, help="Semana (S1..S24), ej. S11")
    ap.add_argument("--index", default=str(INDEX_PATH), help="Ruta al YAML (resources/videos.yml)")
    ap.add_argument("--calendar", default=str(CALENDAR_PATH), help="Ruta a Calendario.md")
    ap.add_argument("--create-if-missing", action="store_true", help="Crear Calendario.md si no existe")
    args = ap.parse_args(argv)

    week = args.week.upper()
    index = load_index(Path(args.index))
    items = videos_for_week(index, week)
    section = build_md_section(week, items)
    inject_into_calendar(week, section, Path(args.calendar), create_if_missing=args.create_if_missing)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
