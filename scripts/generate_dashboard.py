import json
import re
from pathlib import Path

def extract_points(col_name):
    match = re.search(r"__(\d+)", col_name)
    return int(match.group(1)) if match else None

def main():
    scripts_dir = Path(__file__).parent
    raw_path = scripts_dir / "data_raw.json"

    with raw_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    columns = raw[0]
    players = []

    for row in raw[1:]:
        if not row or len(row) < 1:
            continue

        name = row[0]
        total_points = 0
        chest_count = 0

        for col_index, col_name in enumerate(columns):
            points_per_item = extract_points(col_name)
            if points_per_item is None:
                continue

            try:
                value = int(row[col_index])
            except:
                value = 0

            total_points += value * points_per_item
            chest_count += value

        players.append({
            "name": name,
            "points": total_points,
            "chests": chest_count
        })

    players.sort(key=lambda p: p["points"], reverse=True)

    repo_root = scripts_dir.parent
    output_path = repo_root / "data.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump({"players": players}, f, ensure_ascii=False, indent=2)

    print(f"Wygenerowano dashboard do {output_path}")

if __name__ == "__main__":
    main()

