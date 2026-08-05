import os
import json
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build


def main():
    # ID arkusza z sekreta
    sheet_id = os.environ["SHEET_ID"]

    # JSON z kluczem serwisowym z sekreta
    creds_json = os.environ["GOOGLE_CREDENTIALS"]
    creds_dict = json.loads(creds_json)

    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    )

    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # Pobieramy cały zakres (nagłówki + dane)
    result = sheet.values().get(
        spreadsheetId=sheet_id,
        range="A1:ZZ999",
    ).execute()

    values = result.get("values", [])

    # Zapisujemy data_raw.json ZAWSZE obok tego pliku (w folderze scripts)
    scripts_dir = Path(__file__).parent
    raw_path = scripts_dir / "data_raw.json"

    with raw_path.open("w", encoding="utf-8") as f:
        json.dump(values, f, ensure_ascii=False, indent=2)

    print(f"Pobrano arkusz do {raw_path}")


if __name__ == "__main__":
    main()


