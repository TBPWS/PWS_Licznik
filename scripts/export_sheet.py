import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

sheet_id = os.environ["SHEET_ID"]

creds_json = os.environ["GOOGLE_CREDENTIALS"]
creds_dict = json.loads(creds_json)

creds = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

result = sheet.values().get(
    spreadsheetId=sheet_id,
    range="A1:ZZ999"
).execute()

values = result.get("values", [])

with open("scripts/data_raw.json", "w", encoding="utf-8") as f:
    json.dump(values, f, ensure_ascii=False, indent=2)

print("Pobrano arkusz do data_raw.json")

