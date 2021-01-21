from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import io

# TODO Login no Google Drive com o OAuth 2.0

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
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


# Como faremos:

# TODO Pega todos os relatórios do banco de dados
DATABASE_SHEET = '1tqXLhhnO1jdvmD6ZHkCizdj946JqexOZmeh48AugtNo'

sheet = sheetsService.spreadsheets()
values = sheet.values().get(spreadsheetId=DATABASE_SHEET, range="A:Z", majorDimension="COLUMNS").execute()
print(values)

# TODO Backup destes dados em uma pasta local
# ~ Processo de formatação manual de arquivos ~ #
# TODO Pega uma pasta de referência dentro do Google Drive:
    # TODO Para cada relatório dentro do banco de dados:
        # TODO Crie um título no formato
        # TODO [DATADORELATORIO]$[CARIMBODATAHORA]$[AREADORELATORIO]
        # TODO Veja se há algum relatório neste formato dentro da pasta selecionada,
        # TODO Se existir, ignore-o e continue
        # TODO Se não existir, crie-o utilizando as informações do banco de dados
    # TODO Para cada arquivo dentro da pasta selecionada:
        # TODO Fazer download para uma pasta local
    # TODO Para cada arquivo dentro da pasta local selecionada
        # TODO Junte cada arquivo e faça o Caderno de Engenharia principal

    # TODO Call the Drive v3 API
    # TODO results = service.files().list(
    # TODO     pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # TODO items = results.get('files', [])


GERADO_FOLDER = '1gJ53q9tAjUoMHbf1YxaMhYE4P6Si-Dsa'
FORMATADO_FOLDER = '1rBm4V_MSWtX2MJwdOR_QH8FW2cbmjaFn'
EMANALISE_FOLDER = '1PJLD_l_0TFOkJVnUI57aufwDRtU4_TLD'
RESOURCES_FOLDER = '1O0ERZ6_WBXBL3HW86EnNIBbDto_1hLO4';

DEFAULT_FOLDER = '1AUDZPuUGHPzBTXGuRTfPezgcdCE6ummk'

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