import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "demo" / "real_industry_eval_questions.json"
OUT_DIR = ROOT / "data" / "demo"

QUICK_12_IDS = [
    "param-004",
    "docintent-001",
    "docintent-005",
    "risk-syn-005",
    "safety-003",
    "insufficient-003",
    "insufficient-004",
    "wo-boundary-001",
    "wo-boundary-002",
    "confuse-003",
    "smoke-006",
    "fault-006",
]

V031_FIX_FOCUS_10_IDS = [
    "smoke-006",
    "docintent-005",
    "safety-005",
    "risk-syn-005",
    "docintent-001",
    "insufficient-003",
    "safety-002",
    "param-001",
    "param-003",
    "wo-boundary-006",
]


def main() -> None:
    items = json.loads(SOURCE.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in items}
    missing = [item_id for item_id in QUICK_12_IDS if item_id not in by_id]
    if missing:
        raise RuntimeError(f"quick dataset ids not found: {missing}")

    quick = [by_id[item_id] for item_id in QUICK_12_IDS]
    focus = [by_id[item_id] for item_id in V031_FIX_FOCUS_10_IDS]
    baseline = items[:24]
    generalization = items

    write_dataset("real_industry_eval_questions_quick_12.json", quick, 12)
    write_dataset("real_industry_eval_questions_v031_fix_focus_10.json", focus, 10)
    write_dataset("real_industry_eval_questions_baseline_24.json", baseline, 24)
    write_dataset("real_industry_eval_questions_generalization_60.json", generalization, 60)


def write_dataset(filename: str, items: list[dict], expected_count: int) -> None:
    if len(items) != expected_count:
        raise RuntimeError(f"{filename} expected {expected_count} items, got {len(items)}")
    path = OUT_DIR / filename
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(items)} questions to {path}")


if __name__ == "__main__":
    main()
