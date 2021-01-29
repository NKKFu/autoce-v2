import pickle
from os import path, makedirs
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import io
import pathlib
from datetime import datetime
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/documents.readonly',
          'https://www.googleapis.com/auth/spreadsheets.readonly']

# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
creds = None
if path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If there are no (valid) credentials available, let the user log in from 
# his default browser
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file ('credentials.json', 
            SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next log in so we don't need to authorize
    # every time we execute this code
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('drive', 'v3', credentials=creds)
sheetsService = build('sheets', 'v4', credentials=creds)
docsService = build('docs', 'v1', credentials=creds)

# Checks if config.json exists
# TODO: Check if all necessary keys exists inside json file
if not path.exists('config.json'):
    Exception('You need provide a config.json')

config = json.load(open('config.json'))

DATABASE_SHEET = config['DATABASE_SHEET']
DEFAULT_FOLDER = config['DEFAULT_FOLDER']

sheet = sheetsService.spreadsheets()

# Count how many columns
values = sheet.values().get(spreadsheetId=DATABASE_SHEET,
                            range="A1:Z1",
                            majorDimension="COLUMNS").execute()['values']
column_quantity = len(values)

# Convert columns quantity to alphabet (1=a, 2=b, 3=b ...)
column_in_char = chr(column_quantity + 96)

# Get all rows in the database
values = sheet.values().get(spreadsheetId=DATABASE_SHEET, 
                            range=f"A2:{column_in_char}999", 
                            majorDimension="ROWS").execute()['values']

# We need to add some columns if it doesn't exist on row
# every single row needs to have same column quantity
for row in values:
    while len(row) < column_quantity:
        row.append("")

# TODO: Put that on the config.json
# Backup of database (folder name)
BACKUP_PATH="backup"
# Backup of generated PDF's  (folder name)
BACKUP_PATH_PDF="backup-pdf"

# Create path if doesn't exist yet
# it will create at same path of this code
if not path.exists(BACKUP_PATH):
    makedirs(BACKUP_PATH)

# Write database backup in format: month.day_hour_minute_second to doesn't conflit to another backup
curr_time = datetime.now()
file_name = f"{curr_time.month}.{curr_time.day}_{curr_time.hour}_{curr_time.minute}_{curr_time.second}"
with open (path.join(pathlib.Path().absolute(), BACKUP_PATH, f"{file_name}.bkp"), 'w') as file:
    file.write(str(values))

# For each row in the database (ignore the first one, based on query)
for index, value in enumerate(values):

    # Some changes because of the date and time format
    # (if doesn't do that, can causes conflicts due the "/")
    date        = str(value[2]).replace("/", "-")
    created_at  = str(value[0]).replace("/", "-")
    area        = str(value[1])

    # Create a default title as format: [DATE]$[CREATED_AT]$[AREA]
    documentTitle = f"{date}${created_at}${area}"
    print(f"Using title: {documentTitle}")

    # Check if is there any document with this title
    results = service.files().list(q = f"'{DEFAULT_FOLDER}' in parents and name='{documentTitle}' and trashed = false", pageSize=1, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    print(f"Found: {str(items)}")

    # If already exist, don't create another
    if (len(items) > 0):
        continue

    # Else, create one using database information
    else:
        # Relations between area and Document ID for template
        # TODO: Change it to list comprehension
        areas = []
        for templateFile in config['TEMPLATE_FILES_ID']:
            # For each file template, get his name and his ID for map every template
            # avaliable on Drive
            areas.append(((templateFile['name'], templateFile['id'])))
        
        # TODO: Change it to list comprehension
        textReplacementsToDo = []
        for fieldIndex, field in enumerate(config['DATABASE_FIELDS_REPRESENTATION']):
            # Get a field and his representation for each correspondent in database column
            # we do that for replace in the document
            textReplacementsToDo.append([field, values[index][fieldIndex]])
        
        # Create a file using the template based on area
        body = {
            'name': documentTitle,
            'parents': [
                DEFAULT_FOLDER
            ]
        }

        # Get templata file ID 
        templateFileId = [x[1] for x in areas if x[0] == area]

        if templateFileId[0] != '':
            templateFileId = templateFileId[0]
        else:
            Exception(f"There is no template string for: {area}")

        currentDocument = service.files().copy(fileId=templateFileId, body=body).execute()
        currentDocumentId = currentDocument.get('id')

        # Do some replacements on placeholder words to database values
        requests = [{
            'replaceAllText': {
                'containsText': {
                    'text': replacement[0],
                    'matchCase':  'true'
                },
                'replaceText': replacement[1]
            }
        } for replacement in textReplacementsToDo]
        docsService.documents().batchUpdate(documentId = currentDocumentId, body={'requests': requests}).execute()

print("Downloading files...")

# Creates backup folder if doesn't exist yet
if not path.exists(BACKUP_PATH_PDF):
    makedirs(BACKUP_PATH_PDF)

responses = service.files().list(q = f"'{DEFAULT_FOLDER}' in parents and trashed = false", fields="nextPageToken, files(id,name)").execute()
for file in responses.get('files', []):
    exists = path.exists(path.join (BACKUP_PATH_PDF, f"{file['name']}.pdf"))

    # Check if we already downloaded this file
    if exists:
        continue
    
    request = service.files().export_media(fileId=file.get('id'),
                                           mimeType='application/pdf')
    fh = io.FileIO(path.join(pathlib.Path().absolute(), BACKUP_PATH_PDF, f"{file.get('name')}.pdf"), 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        done = downloader.next_chunk()

# TODO: Merge everything to only one document

# TODO: Make this code a class
# if __name__ == '__main__':
#     main()