from googleapiclient.discovery import build
from google.oauth2 import service_account
from .models import Citizen, LastFetchedRow
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials', 'credentials.json')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '14JONXoGqMrSqUJR6zFFz05thLz52Ex-Yka1o8BCaPuc'


def read_data_from_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=SCOPES
    )
    sheets_service = build('sheets', 'v4', credentials=credentials)

    # Retrieve the last fetched row from the database
    last_fetched_row = LastFetchedRow.objects.first()
    start_row = last_fetched_row.row_number if last_fetched_row else 1  # Start from the second row if no previous fetch

    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=f'Form!A{start_row}:H'
        ).execute()
        values = result.get('values', [])

        if values:
            non_empty_rows = [row for row in values if any(cell != '' for cell in row)]
            insert_data_to_database(non_empty_rows[1:])
            # Update the last fetched row in the database
            LastFetchedRow.objects.update_or_create(defaults={'row_number': (start_row + len(values))-1}, id=1)
            return non_empty_rows
        else:
            return []
    except Exception as e:
        raise e


def insert_data_to_database(data):
    for row in data:
        try:
            while len(row) < 8:
                row.append('')
            timestamp, name, email, address, phone, adhar, epic, no_response = row
            timestamp = timestamp or None
            name = name or None
            email = email or None
            address = address or None
            phone = phone or None
            adhar = adhar or None
            epic = epic or None
            no_response = no_response or None
            Citizen.objects.create(
                timestamp=timestamp,
                name=name,
                email=email,
                address=address,
                phone=phone,
                adhar=adhar,
                epic=epic,
                no_response=no_response
            )
        except Exception as e:
            # Handle the exception here, e.g., log the error or take appropriate action
            print(f"Error inserting data: {e}")

#
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
# from .models import Citizen
#
# CREDENTIALS_PATH = 'credentials/credentials.json'
#
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# SPREADSHEET_ID = '14JONXoGqMrSqUJR6zFFz05thLz52Ex-Yka1o8BCaPuc'
#
#
# def read_data_from_google_sheets():
#     credentials = service_account.Credentials.from_service_account_file(
#         CREDENTIALS_PATH, scopes=SCOPES
#     )
#     sheets_service = build('sheets', 'v4', credentials=credentials)
#
#     try:
#         result = sheets_service.spreadsheets().values().get(
#             spreadsheetId=SPREADSHEET_ID, range='Form'
#         ).execute()
#         values = result.get('values', [])
#
#         if values:
#             non_empty_rows = [row for row in values if any(cell != '' for cell in row)]
#             insert_data_to_database(non_empty_rows[1:])
#             return non_empty_rows
#         else:
#             return []
#     except Exception as e:
#         raise e
#
#
# def insert_data_to_database(data):
#     for row in data:
#         try:
#             while len(row) < 8:
#                 row.append('')
#             timestamp, name, email, address, phone, adhar, epic, no_response = row
#             timestamp = timestamp or None
#             name = name or None
#             email = email or None
#             address = address or None
#             phone = phone or None
#             adhar = adhar or None
#             epic = epic or None
#             no_response = no_response or None
#             Citizen.objects.create(
#                 timestamp=timestamp,
#                 name=name,
#                 email=email,
#                 address=address,
#                 phone=phone,
#                 adhar=adhar,
#                 epic=epic,
#                 no_response=no_response
#             )
#         except Exception as e:
#             # Handle the exception here, e.g., log the error or take appropriate action
#             print(f"Error inserting data: {e}")