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
        self.records = None
        self.get_records()

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
        
    def get_assignments(self):
        self.get_records()
        try:
            return list(self.records['Assignment'])
        except Exception as e:
            print(f"Error fetching assignments: {e}")
            return []
    
    def get_description(self, assignment):
        self.get_records()
        try:
            return self.records.loc[self.records['Assignment'] == assignment, 'Description'].values[0]
        except Exception as e:
            print(f"Error fetching description for {assignment}: {e}")
            return None

    def get_due_date(self, assignment):
        self.get_records()
        try:
            return self.records.loc[self.records['Assignment'] == assignment, 'Due Date'].values[0]
        except Exception as e:
            print(f"Error fetching due date for {assignment}: {e}")
            return None
    
    def get_progress(self, assignment):
        self.get_records()
        try:
            return self.records.loc[self.records['Assignment'] == assignment, 'Progress'].values[0]
        except Exception as e:
            print(f"Error fetching progress for {assignment}: {e}")
            return None
    
    def get_assignee(self, assignment):
        self.get_records()
        try:
            return self.records.loc[self.records['Assignment'] == assignment, 'Assignee Name'].values[0]
        except Exception as e:
            print(f"Error fetching assignee for {assignment}: {e}")
            return None

    def update_record(self, assignment, file_path, description=None, due_date=None, progress=None, assignee=None):
        self.get_records()
        try:
            if not description:
                description = self.get_description(assignment)
            if not due_date:
                due_date = self.get_due_date(assignment)
            if not progress:
                progress = self.get_progress(assignment)
            if not assignee:
                assignee = self.get_assignee(assignment)

            index = self.records[self.records['Assignment'] == assignment].index[0] + 2
            self.worksheet.update(f"B{index}:F{index}", [[description, due_date, progress, assignee, file_path]])
            print(f"Record for {assignment} updated successfully.")
        except Exception as e:
            print(f"Error updating record for {assignment}: {e}")