from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

# Reutiliza las funciones del inyector por semana
try:
    from tools.inject_videos import (  # importa desde paquete tools
        load_index,          # carga resources/videos.yml
        videos_for_week,     # selecciona videos por semana
        build_md_section,    # genera la sección Markdown "Videos base — Sxx"
        inject_into_calendar,# inserta/reemplaza en Calendario.md (con backup)
        INDEX_PATH as DEFAULT_INDEX_PATH,
        CALENDAR_PATH as DEFAULT_CALENDAR_PATH,
    )
except Exception as e:
    print(
        "ERROR: No se pudo importar tools/inject_videos.py.\n"
        "Asegúrate de que existe y que ejecutas este script desde la RAÍZ del repo.\n"
        f"Detalle: {e}",
        file=sys.stderr,
    )
    raise


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Inyecta 'Videos base' (resources/videos.yml) para múltiples semanas en Calendario.md"
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="Inyectar S1..S24")
    g.add_argument("--range", nargs=2, metavar=("FROM", "TO"), help="Rango inclusivo (ej. --range S3 S8)")
    g.add_argument("--weeks", nargs="+", metavar="Sxx", help="Lista explícita (ej. --weeks S2 S5 S11)")

    p.add_argument("--index", default=str(DEFAULT_INDEX_PATH), help="Ruta a resources/videos.yml")
    p.add_argument("--calendar", default=str(DEFAULT_CALENDAR_PATH), help="Ruta a Calendario.md")
    p.add_argument("--create-if-missing", action="store_true", help="Crear Calendario.md si no existe")
    return p.parse_args()


def norm_week(w: str) -> str:
    w = w.strip().upper()
    if not w.startswith("S"):
        raise ValueError(f"Semana inválida: {w} (usa S1..S24)")
    return w


def weeks_from_range(wfrom: str, wto: str) -> List[str]:
    wf, wt = norm_week(wfrom), norm_week(wto)
    sf, st = int(wf[1:]), int(wt[1:])
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
        weeks = [norm_week(w) for w in args.weeks]

    index = load_index(Path(args.index))
    calendar = Path(args.calendar)

    if not calendar.exists() and not args.create_if_missing:
        print(
            f"ERROR: No existe {calendar}. Usa --create-if-missing o créalo manualmente.",
            file=sys.stderr,
        )
        return 2

    count = 0
    for w in weeks:
        items = videos_for_week(index, w)
        section = build_md_section(w, items)
        inject_into_calendar(
            week=w,
            section_md=section,
            calendar_path=calendar,
            create_if_missing=args.create_if_missing,
        )
        count += 1

    print(f"Listo: inyectadas {count} semanas de VIDEOS en {calendar}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
