import os
import json
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

SPARQL_URL = os.getenv("WIKIDATA_SPARQL_URL", "https://query.wikidata.org/sparql")
HEADERS = {"User-Agent": "OpenDataFitHou/1.0 (contact@example.com)"}

SPARQL_TEMPLATE = """
SELECT ?label_vi ?label_en ?desc_vi ?instanceOf WHERE {{
  wd:{qid} rdfs:label ?label .
  FILTER(LANG(?label) IN (\"vi\", \"en\"))
  OPTIONAL {{ wd:{qid} schema:description ?desc . FILTER(LANG(?desc) = \"vi\") }}
  OPTIONAL {{ wd:{qid} wdt:P31 ?instanceOf }}
  BIND(IF(LANG(?label) = \"vi\", ?label, "") AS ?label_vi)
  BIND(IF(LANG(?label) = \"en\", ?label, "") AS ?label_en)
  BIND(IF(BOUND(?desc), ?desc, "") AS ?desc_vi)
}}
"""

def fetch_wikidata_entity(qid):
    query = SPARQL_TEMPLATE.format(qid=qid)
    params = {"query": query, "format": "json"}
    r = requests.get(SPARQL_URL, params=params, headers=HEADERS)
    r.raise_for_status()
    results = r.json()["results"]["bindings"]
    label = {"vi": "", "en": ""}
    desc = ""
    instance_of = ""
    for row in results:
        if "label_vi" in row and row["label_vi"].get("value"):
            label["vi"] = row["label_vi"]["value"]
        if "label_en" in row and row["label_en"].get("value"):
            label["en"] = row["label_en"]["value"]
        if "desc_vi" in row and row["desc_vi"].get("value"):
            desc = row["desc_vi"]["value"]
        if "instanceOf" in row and row["instanceOf"].get("value"):
            instance_of = row["instanceOf"]["value"].split("/")[-1]
    return {
        "label": label,
        "description": desc,
        "instance_of": instance_of
    }

def fetch_multiple_entities(qids):
    result = {}
    for qid in qids:
        try:
            print(f"Fetching {qid} ...")
            result[qid] = fetch_wikidata_entity(qid)
        except Exception as e:
            print(f"Failed {qid}: {e}")
    return result

def save_entities_json(data):
    outdir = Path("data/raw/wikidata")
    outdir.mkdir(parents=True, exist_ok=True)
    fname = datetime.utcnow().strftime("%Y-%m-%d") + "_wikidata_entities.json"
    fpath = outdir / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {fpath}")

if __name__ == "__main__":
    # Ví dụ: 5 QIDs phổ biến
    qids = ["Q16917", "Q3918", "Q12418", "Q43229", "Q33506"]
    entities = fetch_multiple_entities(qids)
    save_entities_json(entities)
