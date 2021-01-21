import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("client_secrets.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Form Caderno de Engenharia (respostas)").sheet1  # Open the spreadhseet

column_quantity = len(sheet.row_values(1))

data = []
current_row = []
for index, value in enumerate(sheet.get_all_values()):
    if (index != 0 or index % column_quantity == 0):
        data.append(current_row)
        current_row = []
    current_row = [*current_row, *value]

