import yaml
from pathlib import Path
from urllib.parse import urlparse

REQ_MIN_KEYS = {"id", "title", "url"}
VALID_DIFFICULTY = {"beginner", "intermediate", "advanced", "mixed"}

def test_videos_yaml_exists_and_structure():
    p = Path("resources/videos.yml")
    assert p.exists(), "Falta resources/videos.yml"
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "videos.yml: la raíz debe ser dict"
    assert "collections" in data and isinstance(data["collections"], dict), "Debe existir 'collections' (dict)"

def test_videos_ids_unique_and_minimal_fields():
    data = yaml.safe_load(Path("resources/videos.yml").read_text(encoding="utf-8"))
    seen_ids = set()
    had_items = False

    for coll_name, items in data["collections"].items():
        assert isinstance(items, list), f"'{coll_name}' debe ser lista"
        for it in items:
            had_items = True
            # Claves mínimas
            missing = REQ_MIN_KEYS - set(it.keys())
            assert not missing, f"[{coll_name}] Falta(n) clave(s): {missing} en item: {it}"
            # ID único
            _id = it["id"]
            assert _id not in seen_ids, f"ID duplicado: {_id}"
            seen_ids.add(_id)
            # URL válida
            u = urlparse(it["url"])
            assert u.scheme in {"http", "https"} and u.netloc, f"URL inválida en {_id}: {it['url']}"
            # Al menos weeks o blocks
            has_weeks = bool(it.get("weeks"))
            has_blocks = bool(it.get("blocks"))
            assert has_weeks or has_blocks, f"{_id}: define 'weeks' y/o 'blocks'"
            # difficulty (si viene) en valores válidos
            if "difficulty" in it and it["difficulty"] is not None:
                assert it["difficulty"] in VALID_DIFFICULTY, f"{_id}: difficulty inválido: {it['difficulty']}"

    assert had_items, "No hay items en 'collections' de videos.yml"
