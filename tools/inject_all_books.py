from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

# Reutilizamos funciones del inyector de libros por semana
try:
    from tools.inject_books import (
        load_index,          # carga resources/books.yml
        books_for_week,      # selecciona libros por semana
        md_section,          # genera la sección Markdown "Lecturas base — Sxx"
        inject,              # inserta/reemplaza en Calendario.md (con backup)
        INDEX as DEFAULT_INDEX_PATH,
        CALENDAR as DEFAULT_CALENDAR_PATH,
    )
except Exception:
    print(
        "ERROR: No se pudo importar tools/inject_books.py. "
        "Asegúrate de que existe y que este script se ejecuta desde la raíz del repo.",
        file=sys.stderr,
    )
    raise


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Inyecta 'Lecturas base' (libros) para múltiples semanas en Calendario.md"
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="Inyectar S1..S24")
    g.add_argument(
        "--range",
        nargs=2,
        metavar=("FROM", "TO"),
        help="Rango inclusivo (ej. --range S10 S14)",
    )
    g.add_argument(
        "--weeks",
        nargs="+",
        metavar="Sxx",
        help="Lista explícita de semanas (ej. --weeks S3 S7 S11)",
    )

    p.add_argument("--index", default=str(DEFAULT_INDEX_PATH), help="Ruta a resources/books.yml")
    p.add_argument("--calendar", default=str(DEFAULT_CALENDAR_PATH), help="Ruta a Calendario.md")
    p.add_argument("--create-if-missing", action="store_true", help="Crear Calendario.md si no existe")
    return p.parse_args()


def normalize_week(w: str) -> str:
    w = w.strip().upper()
    if not w.startswith("S"):
        raise ValueError(f"Semana inválida: {w} (usa formato S1..S24)")
    return w


def weeks_from_range(wfrom: str, wto: str) -> List[str]:
    wf = normalize_week(wfrom)
    wt = normalize_week(wto)
    sf = int(wf[1:])
    st = int(wt[1:])
    if sf < 1 or st > 24 or sf > st:
        raise ValueError("Rango fuera de límites (1..24) o invertido")
    return [f"S{i}" for i in range(sf, st + 1)]


def main(argv: List[str] | None = None) -> int:
    args = parse_args()

    if args.all:
        weeks = [f"S{i}" for i in range(1, 25)]
    elif args.range:
        weeks = weeks_from_range(args.range[0], args.range[1])
    else:
        weeks = [normalize_week(w) for w in args.weeks]

    index = load_index(Path(args.index))
    calendar_path = Path(args.calendar)

    if not calendar_path.exists() and not args.create_if_missing:
        print(
            f"ERROR: No existe {calendar_path}. Usa --create-if-missing o créalo manualmente.",
            file=sys.stderr,
        )
        return 2

    count = 0
    for w in weeks:
        items = books_for_week(index, w)
        section = md_section(w, items)
        inject(week=w, section_md=section, calendar=calendar_path, create=args.create_if_missing)
        count += 1

    print(f"Listo: inyectadas {count} semanas de LIBROS en {calendar_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
