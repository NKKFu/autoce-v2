from __future__ import print_function
import pickle
from os import path, makedirs
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import io
import pathlib
from datetime import datetime

# TODO Login no Google Drive com o OAuth 2.0

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/documents.readonly',
          'https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next log in
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('drive', 'v3', credentials=creds)
sheetsService = build('sheets', 'v4', credentials=creds)
docsService = build('docs', 'v1', credentials=creds)

DATABASE_SHEET = '1tqXLhhnO1jdvmD6ZHkCizdj946JqexOZmeh48AugtNo'
DEFAULT_FOLDER = '1AUDZPuUGHPzBTXGuRTfPezgcdCE6ummk'

TEMPLATE_ENGINEERING = '1xED809H0-AgtPwJRPtr-piBhCYRl0ZbkPAJXjxN0LWI'
TEMPLATE_BUSINESSPLAN = '1Fz9bdTujxcQmA03iUFt8mGgvvV2_4mc6HsmD4i0Tw-k'
TEMPLATE_TEAMWORK = '1YOVMBbSXPFGIneTFW8XNJXOO2ilZYTeq1VmGf77NoGU';

# Como faremos:

# Pega todos os relatórios do banco de dados
sheet = sheetsService.spreadsheets()

# Contagem de colunas na primeira row
values = sheet.values().get(spreadsheetId=DATABASE_SHEET, range="A1:Z1", majorDimension="COLUMNS").execute()['values']
column_quantity = len(values)
column_in_char = chr(column_quantity + 96)

values = sheet.values().get(spreadsheetId=DATABASE_SHEET, range=f"A2:{column_in_char}999", majorDimension="ROWS").execute()['values']

# Todos terao a mesma quantidade de elementos
for row in values:
    while len(row) < column_quantity:
        row.append("")

# Backup destes dados em uma pasta local
BACKUP_PATH="backup"
BACKUP_PATH_PDF="backup-pdf"

if not path.exists(BACKUP_PATH):
    makedirs(BACKUP_PATH)

file_name = f"{datetime.now().day}.{datetime.now().day}_{datetime.now().hour}_{datetime.now().minute}_{datetime.now().second}"
with open (path.join(pathlib.Path().absolute(), BACKUP_PATH, f"{file_name}.bkp"), 'w') as file:
    file.write(str(values))

# ~ Processo de formatação manual de arquivos ~ #

# Para cada relatório dentro do banco de dados:
# Ignora o header
for value in values:
    # TODO Crie um título no formato: [DATADORELATORIO]$[CARIMBODATAHORA]$[AREADORELATORIO]

    # Formatação
    date = str(value[2]).replace("/", "-")
    created_at = str(value[0]).replace("/", "-")
    area = str(value[1])

    documentTitle = f"{date}${created_at}${area}"
    print(documentTitle)

    # TODO Pega uma pasta de referência dentro do Google Drive:
    # TODO Veja se há algum relatório neste formato dentro da pasta selecionada,
    results = service.files().list(q = f"'{DEFAULT_FOLDER}' in parents and name='{documentTitle}' and trashed = false", pageSize=1, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    print(items)

    # Relação de áreas e uid dos documentos
    areas = {
        'Trabalho em equipe': TEMPLATE_TEAMWORK,
        'Engenharia': TEMPLATE_ENGINEERING,
        'Plano de Negócios': TEMPLATE_BUSINESSPLAN
    }

    # Área do relatório
    area = value[1]

    # TODO Se existir, ignore-o e continue
    if (len(items) > 0):
        continue

    # TODO Se não existir, crie-o utilizando as informações do banco de dados
    else:

        # Define propriedades do documento
        [created_at, area, date, time, author, participants, title, description, images, hashtags, what1, why1, when1, what2, why2, when2, what3, why3, when3] = value;

        textReplacementsToDo = [
            ['«DATA»', date],
            ['«HORARIO»', time],
            ['«AUTOR»', author],
            ['«PARTICIPANTES»', participants],
            ['«ASSUNTO»', title],
            ['«DESCRICAO»', description],
            ['«IMAGENS»', images],
            ['«OQUE1»', what1],
            ['«PORQUE1»', why1],
            ['«PRAZO1»', when1],
            ['«OQUE2»', what2],
            ['«PORQUE2»', why2],
            ['«PRAZO2»', when2],
            ['«OQUE3»', what3],
            ['«PORQUE3»', why3],
            ['«PRAZO3»', when3],
            ['«HASHTAGS»', hashtags]
        ]

        # Documento template
        template_document = docsService.documents().get(documentId=areas[area]).execute()

        # Replace nos textos
        body = {
            'name': documentTitle,
            'parents': [
                DEFAULT_FOLDER
            ]
        }

        currentDocument = service.files().copy(fileId=areas[area], body=body).execute()
        currentDocumentId = currentDocument.get('id')

        requests = []
        for replacement in textReplacementsToDo:
            requests.append({
                'replaceAllText': {
                    'containsText': {
                        'text': replacement[0],
                        'matchCase':  'true'
                    },
                    'replaceText': replacement[1]
                }
            })

        docsService.documents().batchUpdate(documentId = currentDocumentId, body={'requests': requests}).execute()

if not path.exists(BACKUP_PATH_PDF):
    makedirs(BACKUP_PATH_PDF)

# TODO Verificar se os arquivos pdf já existem

responses = service.files().list(q = f"'{DEFAULT_FOLDER}' in parents and trashed = false", fields="nextPageToken, files(id,name)").execute()
for file in responses.get('files', []):
    request = service.files().export_media(fileId=file.get('id'),
                                           mimeType='application/pdf')
    fh = io.FileIO(path.join(pathlib.Path().absolute(), BACKUP_PATH_PDF, f"{file.get('name')}.pdf"), 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        done = downloader.next_chunk()
    # TODO Para cada arquivo dentro da pasta local selecionada
        # TODO Junte cada arquivo e faça o Caderno de Engenharia principal

GERADO_FOLDER = '1gJ53q9tAjUoMHbf1YxaMhYE4P6Si-Dsa'
FORMATADO_FOLDER = '1rBm4V_MSWtX2MJwdOR_QH8FW2cbmjaFn'
EMANALISE_FOLDER = '1PJLD_l_0TFOkJVnUI57aufwDRtU4_TLD'
RESOURCES_FOLDER = '1O0ERZ6_WBXBL3HW86EnNIBbDto_1hLO4';

TEMPLATE_ENGINEERING = '1xED809H0-AgtPwJRPtr-piBhCYRl0ZbkPAJXjxN0LWI'
TEMPLATE_BUSINESSPLAN = '1Fz9bdTujxcQmA03iUFt8mGgvvV2_4mc6HsmD4i0Tw-k'
TEMPLATE_TEAMWORK = '1YOVMBbSXPFGIneTFW8XNJXOO2ilZYTeq1VmGf77NoGU';

PARENTFILE_DOCUMENT = '15I8KBPShS7iXrzEs_Xm_1iBtgvon6v3KXzorycZHUt8';

ENGINEERINGCOVER_DOCUMENT = '1a26hcaIzrlJCZcQ0y3oc8cmTggqeFHUQjej1vKPv2x8'
BUSINESSPLANCOVER_DOCUMENT = '1SF5eAEj_yD-_pbb2Oc_UHoIWqgMrk5cDv_YRfF7134Q'
TEAMWORKINGCOVER_DOCUMENT = '1ZWlRuzVDc33xFOEGOoeUjpzIQrKFrX7tB-eqyZcMdk0';

MAINFILENAME_STRING = 'Caderno de Engenharia';

# if __name__ == '__main__':
#     main()
