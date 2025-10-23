from __future__ import annotations
import argparse, sys
from pathlib import Path
from typing import Any, Dict, List
import yaml  # type: ignore

INDEX = Path("resources/books.yml")

def load_index() -> Dict[str, Any]:
    if not INDEX.exists():
        sys.exit("ERROR: no existe resources/books.yml")
    return yaml.safe_load(INDEX.read_text(encoding="utf-8"))

def select(colls: List[List[Dict[str,Any]]], week: str|None, block: str|None, topics: List[str]) -> List[Dict[str,Any]]:
    out: List[Dict[str,Any]] = []
    for items in colls:
        for it in items:
            ok = True
            if week:
                ok &= week in (it.get("weeks") or [])
            if block:
                ok &= block in (it.get("blocks") or [])
            if topics:
                need = {t.lower() for t in topics}
                has = {t.lower() for t in (it.get("topics") or [])}
                ok &= bool(need <= has or need & has)
            if ok:
                out.append(it)
    out.sort(key=lambda d: d.get("title","").lower())
    return out

def to_md(week: str|None, items: List[Dict[str,Any]]) -> str:
    title = f"### Lecturas base — {week}" if week else "### Lecturas base"
    lines = [title, ""]
    if not items:
        lines.append("_(No se encontraron libros para este filtro)_")
        return "\n".join(lines)
    for it in items:
        title = it.get("title","Sin título")
        author = it.get("author","")
        url = it.get("url")
        lp = it.get("local_path")
        link = url or (f"`{lp}`" if lp else "#")
        topics = ", ".join(it.get("topics") or [])
        meta = []
        if it.get("year"): meta.append(str(it["year"]))
        if it.get("lang"): meta.append(it["lang"])
        meta_str = f" ({', '.join(meta)})" if meta else ""
        lines.append(f"- [{title}]({link}) — {author}{meta_str} — temas: {topics}")
    return "\n".join(lines)

def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("-w","--week", help="Semana S1..S24")
    g.add_argument("-b","--block", help="Bloque B1..B5A/B5B")
    ap.add_argument("-t","--topics", nargs="*", default=[])
    args = ap.parse_args(argv)

    data = load_index()
    colls = list((data.get("collections") or {}).values())
    week = args.week.upper() if args.week else None
    block = args.block.upper() if args.block else None
    items = select(colls, week, block, args.topics)
    print(to_md(week, items))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
