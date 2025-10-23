from __future__ import annotations

import argparse
import sys
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception as e:  # pragma: no cover
    print("ERROR: PyYAML no está instalado. Ejecuta:\n  python -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)


INDEX_PATH = Path("resources/videos.yml")


def load_index(path: Path = INDEX_PATH) -> Dict[str, Any]:
    if not path.exists():
        print(f"ERROR: No existe el archivo {path}.", file=sys.stderr)
        sys.exit(2)
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def by_week(index: Dict[str, Any], week: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    collections = index.get("collections", {}) or {}
    for items in collections.values():
        for item in items:
            if week in (item.get("weeks") or []):
                out.append(item)
    return out


def by_block(index: Dict[str, Any], block: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    collections = index.get("collections", {}) or {}
    for items in collections.values():
        for item in items:
            if block in (item.get("blocks") or []):
                out.append(item)
    return out


def filter_topics(items: List[Dict[str, Any]], topics: List[str]) -> List[Dict[str, Any]]:
    if not topics:
        return items
    need = {t.strip().lower() for t in topics if t.strip()}
    out = []
    for it in items:
        has = {t.lower() for t in (it.get("topics") or [])}
        if need <= has or need & has:
            out.append(it)
    return out


def md_section(week: str | None, items: List[Dict[str, Any]]) -> str:
    header = f"### Videos base — {week}" if week else "### Videos base"
    lines = [header, ""]
    if not items:
        lines.append("_(No se encontraron videos para los filtros dados)_")
        return "\n".join(lines)

    # Ordena por título
    items = sorted(items, key=lambda d: d.get("title", "").lower())

    for v in items:
        title = v.get("title", "Sin título")
        url = v.get("url", "#")
        topics = ", ".join(v.get("topics") or [])
        ts = v.get("timestamps") or {}
        ts_inline = ""
        if isinstance(ts, dict) and ts:
            ts_inline = " · " + ", ".join(f"{k}: {val}" for k, val in ts.items())
        lines.append(f"- [{title}]({url}) — temas: {topics}{ts_inline}")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="suggest_videos",
        description="Genera la sección 'Videos base' en Markdown desde resources/videos.yml.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--week", "-w", help="Semana (S1..S24), ej. S11")
    g.add_argument("--block", "-b", help="Bloque (B1..B5A/B5B), ej. B5A")
    p.add_argument(
        "--topics",
        "-t",
        nargs="*",
        default=[],
        help="Filtrar por temas (intersección), ej: -t fastapi crud oauth2",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Salir con código 3 si no hay resultados (útil en CI).",
    )
    return p.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    index = load_index()

    if args.week:
        items = by_week(index, args.week.upper())
        scope = args.week.upper()
    else:
        items = by_block(index, args.block.upper())
        scope = args.block.upper()

    items = filter_topics(items, args.topics)

    section = md_section(args.week.upper() if args.week else None, items)
    print(section)

    if args.strict and not items:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
