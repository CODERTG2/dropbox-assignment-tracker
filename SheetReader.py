import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

class SheetReader:
    def __init__(self, credentials_path, spreadsheet_id):
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self.authenticate()
        self.get_spreadsheet()
        self.worksheet = self.spreadsheet.get_worksheet(0)
        self.records = self.get_records()
    
    def authenticate(self):
        try:
            credentials = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
            self.client = gspread.authorize(credentials)
        except Exception as e:
            print(f"Error during authentication: {e}")
    
    def get_spreadsheet(self):
        try:
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
        except Exception as e:
            print(f"Error accessing spreadsheet: {e}")
    
    def get_records(self):
        try:
            records = self.worksheet.get_all_records()
            self.records = pd.DataFrame(records)
            return self.records
        except Exception as e:
            print(f"Error fetching records: {e}")
            return []
    
