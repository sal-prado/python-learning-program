from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

# Reutilizamos las funciones del inyector por semana
try:
    from inject_videos import (
        load_index,
        videos_for_week,
        build_md_section,
        inject_into_calendar,
        INDEX_PATH,
        CALENDAR_PATH,
    )
except Exception as e:
    print(
        "ERROR: No se pudo importar inject_videos.py. "
        "Asegúrate de que tools/inject_videos.py existe y es importable.",
        file=sys.stderr,
    )
    raise


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Inyecta 'Videos base' para múltiples semanas (S1..S24) en Calendario.md"
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="Inyectar S1..S24")
    g.add_argument(
        "--range",
        nargs=2,
        metavar=("FROM", "TO"),
        help="Rango inclusive (ej. --range S10 S14)",
    )
    g.add_argument(
        "--weeks",
        nargs="+",
        metavar="Sxx",
        help="Lista explícita de semanas (ej. --weeks S3 S7 S11)",
    )

    p.add_argument("--index", default=str(INDEX_PATH), help="Ruta a resources/videos.yml")
    p.add_argument("--calendar", default=str(CALENDAR_PATH), help="Ruta a Calendario.md")
    p.add_argument(
        "--create-if-missing",
        action="store_true",
        help="Crear Calendario.md si no existe",
    )
    return p.parse_args(argv)


def normalize_week(w: str) -> str:
    w = w.strip().upper()
    if not w.startswith("S"):
        raise ValueError(f"Semana inválida: {w} (usa formato S1..S24)")
    return w


def weeks_from_range(wfrom: str, wto: str) -> List[str]:
    wf = normalize_week(wfrom)
    wt = normalize_week(wto)
    try:
        sf = int(wf[1:])
        st = int(wt[1:])
    except ValueError:
        raise ValueError("Rango inválido: usa S1..S24")
    if sf < 1 or st > 24 or sf > st:
        raise ValueError("Rango fuera de límites (1..24) o invertido")
    return [f"S{i}" for i in range(sf, st + 1)]


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    if args.all:
        weeks = [f"S{i}" for i in range(1, 25)]
    elif args.range:
        weeks = weeks_from_range(args.range[0], args.range[1])
    else:
        weeks = [normalize_week(w) for w in args.weeks]

    index = load_index(Path(args.index))

    cal_path = Path(args.calendar)
    if not cal_path.exists() and not args.create_if_missing:
        print(
            f"ERROR: No existe {cal_path}. Pásale --create-if-missing "
            "o crea el archivo manualmente.",
            file=sys.stderr,
        )
        return 2

    # Inyectar semana a semana
    ok = 0
    for w in weeks:
        items = videos_for_week(index, w)
        section = build_md_section(w, items)
        inject_into_calendar(
            week=w,
            section_md=section,
            calendar_path=cal_path,
            create_if_missing=args.create_if_missing,
        )
        ok += 1

    print(f"Listo: inyectadas {ok} semanas en {cal_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
