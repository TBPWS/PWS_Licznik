import json
import re

# Wczytaj dane z Google Sheets
with open("data_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

# Pierwszy wiersz = nazwy kolumn
columns = raw[0]

players = []

# Funkcja do wyciągania wartości punktowej z nazwy kolumny
def extract_points(col_name):
    match = re.search(r"__(\d+)", col_name)
    return int(match.group(1)) if match else None

# Przetwarzanie każdego gracza
for row in raw[1:]:
    if not row or len(row) < 3:
        continue

    name = row[0]
    total_points = 0
    chest_count = 0

    # Iteracja po wszystkich kolumnach
    for col_index, col_name in enumerate(columns):
        # Kolumny skrzyń mają format "__XX"
        points_per_item = extract_points(col_name)
        if points_per_item is None:
            continue  # pomijamy kolumny bez punktów

        # wartość w komórce
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

# Zapisz wynik do data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump({"players": players}, f, ensure_ascii=False, indent=2)

print("Wygenerowano data.json")

