from __future__ import annotations
import argparse, sys, re, datetime as dt
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception:
    print("ERROR: PyYAML no está instalado. Ejecuta: python -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)

INDEX = Path("resources/books.yml")
CALENDAR = Path("Calendario.md")


def load_index(path: Path) -> Dict[str, Any]:
    if not path.exists():
        sys.exit(f"ERROR: no existe {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def books_for_week(index: Dict[str, Any], week: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for items in (index.get("collections") or {}).values():
        for it in items:
            if week in (it.get("weeks") or []):
                out.append(it)
    out.sort(key=lambda d: d.get("title", "").lower())
    return out


def md_section(week: str, items: List[Dict[str, Any]]) -> str:
    lines = [f"### Lecturas base — {week}", ""]
    if not items:
        lines.append("_(No se encontraron libros para esta semana en resources/books.yml)_")
        return "\n".join(lines) + "\n"
    for it in items:
        title = it.get("title", "Sin título")
        author = it.get("author", "")
        url = it.get("url")
        lp = it.get("local_path")
        link = url or (f"`{lp}`" if lp else "#")
        topics = ", ".join(it.get("topics") or [])
        meta = []
        if it.get("year"):
            meta.append(str(it["year"]))
        if it.get("lang"):
            meta.append(it["lang"])
        meta_str = f" ({', '.join(meta)})" if meta else ""
        lines.append(f"- [{title}]({link}) — {author}{meta_str} — temas: {topics}")
    lines.append("")
    return "\n".join(lines) + "\n"


def _backup(path: Path) -> None:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    b = path.with_suffix(path.suffix + f".books.bak-{ts}")
    if path.exists():
        b.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"(Backup: {b.name})")


def inject(week: str, section_md: str, calendar: Path, create: bool) -> None:
    if not calendar.exists():
        if not create:
            sys.exit(f"ERROR: falta {calendar}. Usa --create-if-missing.")
        calendar.write_text("# Calendario del Programa\n\n", encoding="utf-8")

    original = calendar.read_text(encoding="utf-8")
    start = f"<!-- BOOKS_BASE:{week} START -->"
    end = f"<!-- BOOKS_BASE:{week} END -->"
    block = f"{start}\n{section_md}{end}\n"

    # Reemplazo por marcadores si existen
    pat = re.compile(rf"(?s){re.escape(start)}.*?{re.escape(end)}")
    if pat.search(original):
        updated = pat.sub(block.strip() + "\n", original)
        if updated != original:
            _backup(calendar)
            calendar.write_text(updated, encoding="utf-8")
            print(f"OK: reemplazado bloque LIBROS para {week}")
            return

    # Insertar bajo encabezado de semana (### Sxx ...)
    h = re.compile(rf"^###\s*{re.escape(week)}\b.*$", re.MULTILINE)
    m = h.search(original)
    if m:
        pos = m.end()
        updated = original[:pos] + "\n\n" + block + original[pos:]
        _backup(calendar)
        calendar.write_text(updated, encoding="utf-8")
        print(f"OK: insertado bloque LIBROS bajo encabezado {week}")
        return

    # Añadir al final
    updated = original.rstrip() + f"\n\n## {week}\n\n" + block
    _backup(calendar)
    calendar.write_text(updated, encoding="utf-8")
    print(f"OK: añadido bloque LIBROS al final ({week}).")


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Inyecta 'Lecturas base' por semana desde resources/books.yml")
    ap.add_argument("-w", "--week", required=True)
    ap.add_argument("--index", default=str(INDEX))
    ap.add_argument("--calendar", default=str(CALENDAR))
    ap.add_argument("--create-if-missing", action="store_true")
    args = ap.parse_args(argv)

    week = args.week.upper()
    idx = load_index(Path(args.index))
    items = books_for_week(idx, week)
    sec = md_section(week, items)
    inject(week, sec, Path(args.calendar), args.create_if_missing)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
