"""Limpieza determinista del grafo mi-criterio: redaccion PII estricta y vinculo de identidad eldaniels = daniel garcia a traves de perfiles publicos laborales (LinkedIn/GitHub). Idempotente."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "graphify-out"

LINKEDIN_URL = "https://www.linkedin.com/in/jos\u00e9-daniel-garc\u00eda-castro-ba44b4314"
GITHUB_URL = "https://github.com/eldaniels13"
REPO_URL = "https://github.com/eldaniels13/mi-criterio"

LABEL_PATTERNS = [
    (re.compile(r"jos[ée]\s+daniel\s+garc[ií]a\s+castro", re.I), "[perfil profesional]"),
    (re.compile(r"jos[ée]\s+daniel", re.I), "[perfil profesional]"),
    (re.compile(r"daniel\s+garc[ií]a", re.I), "[perfil profesional]"),
    (re.compile(r"garc[ií]a\s+castro", re.I), "[perfil profesional]"),
    (re.compile(r"\biteso\b", re.I), "[universidad]"),
    (re.compile(r"iteso", re.I), "[universidad]"),
    (re.compile(r"\bupm\b", re.I), "[universidad]"),
    (re.compile(r"\bmadrid\b", re.I), "[ciudad]"),
    (re.compile(r"colegio\s+guadalajara", re.I), "[escuela]"),
    (re.compile(r"colegio\s+claret", re.I), "[escuela]"),
    (re.compile(r"\bguadalajara\b", re.I), "[ciudad]"),
    (re.compile(r"\bjalisco\b", re.I), "[ciudad]"),
    (re.compile(r"\bzapopan\b", re.I), "[ciudad]"),
    (re.compile(r"\bgdl\b", re.I), "[ciudad]"),
    (re.compile(r"\+?\d[\d\s\-().]{7,}\d"), "[redactado]"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[a-z]{2,}"), "[redactado]"),
]

ID_PATTERNS = [
    (re.compile(r"jose_daniel_garcia_castro"), "perfil_profesional"),
    (re.compile(r"jose_daniel"), "perfil_profesional"),
    (re.compile(r"daniel_garcia"), "perfil_profesional"),
    (re.compile(r"garcia_castro"), "perfil_profesional"),
    (re.compile(r"\biteso\b"), "universidad"),
    (re.compile(r"iteso"), "universidad"),
    (re.compile(r"\bupm\b"), "universidad"),
    (re.compile(r"\bmadrid\b"), "ciudad"),
    (re.compile(r"colegio_guadalajara"), "escuela"),
    (re.compile(r"colegio_claret"), "escuela"),
    (re.compile(r"\bguadalajara\b"), "ciudad"),
    (re.compile(r"\bjalisco\b"), "ciudad"),
    (re.compile(r"\bzapopan\b"), "ciudad"),
]


def redact_label(label):
    text = label
    for pat, repl in LABEL_PATTERNS:
        text = pat.sub(repl, text)
    return re.sub(r"\s+", " ", text).strip()


def redact_id(node_id):
    nid = node_id
    for pat, repl in ID_PATTERNS:
        nid = pat.sub(repl, nid)
    return nid


def main():
    extract_path = OUT / ".graphify_extract.json"
    old_graph_path = OUT / "graph.json"
    data = json.loads(extract_path.read_text())

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    hyperedges = list(data.get("hyperedges", []))

    if old_graph_path.exists():
        old = json.loads(old_graph_path.read_text())
        seen_he = {h.get("id") for h in hyperedges}
        for h in old.get("hyperedges", []):
            if h.get("id") not in seen_he:
                hyperedges.append(h)

    redactions = 0
    for n in nodes:
        sf = n.get("source_file")
        if sf and isinstance(sf, str) and sf.startswith("/home/"):
            n["source_file"] = sf.replace("/home/eldaniels/Codes/mi-criterio/", "")
        if isinstance(n.get("label"), str):
            new_label = redact_label(n["label"])
            if new_label != n["label"]:
                redactions += 1
                n["label"] = new_label

    id_map = {}
    seen = set()
    for n in nodes:
        old_id = n["id"]
        new_id = redact_id(old_id)
        if new_id in seen:
            id_map[old_id] = new_id
            n["_drop"] = True
            continue
        seen.add(new_id)
        n["id"] = new_id
        id_map[old_id] = new_id

    nodes = [n for n in nodes if not n.get("_drop")]

    seen_edges = set()
    clean_edges = []
    for e in edges:
        s, t = id_map.get(e["source"], e["source"]), id_map.get(e["target"], e["target"])
        key = (s, t, e.get("relation"))
        if key in seen_edges:
            continue
        seen_edges.add(key)
        e["source"], e["target"] = s, t
        if isinstance(e.get("source_file"), str) and e["source_file"].startswith("/home/"):
            e["source_file"] = e["source_file"].replace("/home/eldaniels/Codes/mi-criterio/", "")
        clean_edges.append(e)

    node_ids = {n["id"] for n in nodes}
    clean_hyperedges = []
    for h in hyperedges:
        h["nodes"] = [id_map.get(x, x) for x in h.get("nodes", [])]
        h["nodes"] = [x for x in h["nodes"] if x in node_ids]
        if isinstance(h.get("label"), str):
            h["label"] = redact_label(h["label"])
        if len(h["nodes"]) >= 3 and h.get("id") not in {x["id"] for x in clean_hyperedges}:
            clean_hyperedges.append(h)

    identity_anchor = "perfil_maestro_eldaniels_identity" if "perfil_maestro_eldaniels_identity" in node_ids else (
        "perfil_maestro_eldaniels_profile" if "perfil_maestro_eldaniels_profile" in node_ids else None)
    cv_hub = "cv2026eng_perfil_profesional"
    if identity_anchor and cv_hub in node_ids:
        policy_nodes = [
            {"id": "perfil_profesional_linkedin", "label": "[perfil profesional] (LinkedIn — perfil público)",
             "file_type": "document", "source_file": "README.md", "source_location": None,
             "source_url": LINKEDIN_URL, "captured_at": None, "author": None, "contributor": None},
            {"id": "eldaniels_github_profile", "label": "eldaniels13 (GitHub — perfil público)",
             "file_type": "document", "source_file": "README.md", "source_location": None,
             "source_url": GITHUB_URL, "captured_at": None, "author": None, "contributor": None},
            {"id": "mi_criterio_repo_publico", "label": "mi-criterio (repositorio público)",
             "file_type": "document", "source_file": "README.md", "source_location": None,
             "source_url": REPO_URL, "captured_at": None, "author": None, "contributor": None},
        ]
        for pn in policy_nodes:
            if pn["id"] not in node_ids:
                nodes.append(pn)
                node_ids.add(pn["id"])
        policy_edges = [
            (identity_anchor, cv_hub, "same_as"),
            (cv_hub, "perfil_profesional_linkedin", "same_as"),
            (identity_anchor, "perfil_profesional_linkedin", "conceptually_related_to"),
            (identity_anchor, "eldaniels_github_profile", "conceptually_related_to"),
            ("perfil_profesional_linkedin", "eldaniels_github_profile", "conceptually_related_to"),
            ("eldaniels_github_profile", "mi_criterio_repo_publico", "conceptually_related_to"),
        ]
        added = 0
        for s, t, rel in policy_edges:
            if s in node_ids and t in node_ids and (s, t, rel) not in seen_edges:
                clean_edges.append({
                    "source": s, "target": t, "relation": rel,
                    "confidence": "EXTRACTED", "confidence_score": 1.0,
                    "source_file": "README.md", "source_location": None, "weight": 1.0,
                })
                seen_edges.add((s, t, rel))
                added += 1
        if "cv2026eng_perfil_profesional" in node_ids:
            for n in nodes:
                if n["id"] == "cv2026eng_perfil_profesional" and not n.get("source_url"):
                    n["source_url"] = LINKEDIN_URL
    else:
        print("WARN: ancla de identidad o hub CV no encontrados; vinculo de identidad omitido")

    data["nodes"] = nodes
    data["edges"] = clean_edges
    data["hyperedges"] = clean_hyperedges
    extract_path.write_text(json.dumps(data, indent=2))

    print(f"Redacciones aplicadas: {redactions}")
    print(f"Nodos: {len(nodes)} | Edges: {len(clean_edges)} | Hyperedges: {len(clean_hyperedges)}")
    print("Vinculo de identidad: eldaniels <-> perfil profesional <-> LinkedIn/GitHub (EXTRACTED, README.md)")


if __name__ == "__main__":
    main()
