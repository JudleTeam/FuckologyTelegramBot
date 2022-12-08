import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheets:
    def __init__(self, credentials_file: str, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file,
            [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
        )
        http_auth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=http_auth)

    def add_customer(self, title, mention, order_id, created_at, price, phone, username, full_name):
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range='data!A1:H1',
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={
                'values': [[title, mention, order_id, str(created_at), price, phone, username, full_name]]
            }
        ).execute()

    def register_user(self, mention, username, full_name):
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range='all_users!A1:C1',
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={
                'values': [[mention, username, full_name]]
            }
        ).execute()
