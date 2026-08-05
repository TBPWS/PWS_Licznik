import json
import re
from pathlib import Path


def extract_points(col_name: str) -> int | None:
    """
    Szuka wzorca '__XX' w nazwie kolumny i zwraca liczbę punktów.
    Np. 'Tartaros Crypt__25' -> 25
    """
    match = re.search(r"__(\d+)", col_name)
    return int(match.group(1)) if match else None


def main():
    scripts_dir = Path(__file__).parent
    raw_path = scripts_dir / "data_raw.json"

    # Wczytujemy surowe dane z arkusza
    with raw_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    if not raw or len(raw) < 2:
        print("Brak danych w arkuszu – za mało wierszy.")
        return

    # Pierwszy wiersz to nagłówki kolumn
    columns = raw[0]
    players: list[dict] = []

    # Przetwarzanie każdego gracza (kolejne wiersze)
    for row in raw[1:]:
        # pomijamy puste / za krótkie wiersze
        if not row or len(row) < 1:
            continue

        name = row[0]
        total_points = 0
        chest_count = 0

        # Iteracja po wszystkich kolumnach
        for col_index, col_name in enumerate(columns):
            # Kolumny skrzyń mają format '__XX'
            points_per_item = extract_points(col_name)
            if points_per_item is None:
                continue  # pomijamy kolumny bez punktów

            # wartość w komórce (liczba skrzyń)
            try:
                value = int(row[col_index])
            except (ValueError, IndexError):
                value = 0

            total_points += value * points_per_item
            chest_count += value

        players.append(
            {
                "name": name,
                "points": total_points,
                "chests": chest_count,
            }
        )

    # Sortujemy graczy po punktach malejąco
    players.sort(key=lambda p: p["points"], reverse=True)

    # Zapisujemy wynik do data.json obok skryptu (lub zmień ścieżkę, jeśli chcesz w root)
    output_path = scripts_dir / "data.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump({"players": players}, f, ensure_ascii=False, indent=2)

    print(f"Wygenerowano dashboard do {output_path}")


if __name__ == "__main__":
    main()

