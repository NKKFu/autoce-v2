GERADO_FOLDER = '1gJ53q9tAjUoMHbf1YxaMhYE4P6Si-Dsa'
FORMATADO_FOLDER = '1rBm4V_MSWtX2MJwdOR_QH8FW2cbmjaFn'
EMANALISE_FOLDER = '1PJLD_l_0TFOkJVnUI57aufwDRtU4_TLD'
RESOURCES_FOLDER = '1O0ERZ6_WBXBL3HW86EnNIBbDto_1hLO4';

DEFAULT_FOLDER = '1AUDZPuUGHPzBTXGuRTfPezgcdCE6ummk'

TEMPLATE_ENGINEERING = '1xED809H0-AgtPwJRPtr-piBhCYRl0ZbkPAJXjxN0LWI'
TEMPLATE_BUSINESSPLAN = '1Fz9bdTujxcQmA03iUFt8mGgvvV2_4mc6HsmD4i0Tw-k'
TEMPLATE_TEAMWORK = '1YOVMBbSXPFGIneTFW8XNJXOO2ilZYTeq1VmGf77NoGU';

DATABASE_SHEET = '1tqXLhhnO1jdvmD6ZHkCizdj946JqexOZmeh48AugtNo'
PARENTFILE_DOCUMENT = '15I8KBPShS7iXrzEs_Xm_1iBtgvon6v3KXzorycZHUt8';

ENGINEERINGCOVER_DOCUMENT = '1a26hcaIzrlJCZcQ0y3oc8cmTggqeFHUQjej1vKPv2x8'
BUSINESSPLANCOVER_DOCUMENT = '1SF5eAEj_yD-_pbb2Oc_UHoIWqgMrk5cDv_YRfF7134Q'
TEAMWORKINGCOVER_DOCUMENT = '1ZWlRuzVDc33xFOEGOoeUjpzIQrKFrX7tB-eqyZcMdk0';

MAINFILENAME_STRING = 'Caderno de Engenharia';

# Como faremos:
# Pega todos os relatórios do banco de dados

# Backup destes dados em uma pasta local
# ~ Processo de formatação manual de arquivos ~ #
# Pega uma pasta de referência dentro do Google Drive:
    # Para cada relatório dentro do banco de dados:
        # Crie um título no formato
        # [DATADORELATORIO]$[CARIMBODATAHORA]$[AREADORELATORIO]
        # Veja se há algum relatório neste formato dentro da pasta selecionada,
        # Se existir, ignore-o e continue
        # Se não existir, crie-o utilizando as informações do banco de dados
    # Para cada arquivo dentro da pasta selecionada:
        # Fazer download para uma pasta local
    # Para cada arquivo dentro da pasta local selecionada
        # Junte cada arquivo e faça o Caderno de Engenharia principal

