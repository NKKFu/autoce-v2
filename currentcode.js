const GERADO_FOLDER = '1gJ53q9tAjUoMHbf1YxaMhYE4P6Si-Dsa',
    FORMATADO_FOLDER = '1rBm4V_MSWtX2MJwdOR_QH8FW2cbmjaFn',
    EMANALISE_FOLDER = '1PJLD_l_0TFOkJVnUI57aufwDRtU4_TLD',
    RESOURCES_FOLDER = '1O0ERZ6_WBXBL3HW86EnNIBbDto_1hLO4';

const TEMPLATE_ENGINEERING = '1xED809H0-AgtPwJRPtr-piBhCYRl0ZbkPAJXjxN0LWI',
    TEMPLATE_BUSINESSPLAN = '1Fz9bdTujxcQmA03iUFt8mGgvvV2_4mc6HsmD4i0Tw-k',
    TEMPLATE_TEAMWORK = '1YOVMBbSXPFGIneTFW8XNJXOO2ilZYTeq1VmGf77NoGU';

const DATABASE_SHEET = '1tqXLhhnO1jdvmD6ZHkCizdj946JqexOZmeh48AugtNo',
    PARENTFILE_DOCUMENT = '15I8KBPShS7iXrzEs_Xm_1iBtgvon6v3KXzorycZHUt8';

const ENGINEERINGCOVER_DOCUMENT = '1a26hcaIzrlJCZcQ0y3oc8cmTggqeFHUQjej1vKPv2x8',
    BUSINESSPLANCOVER_DOCUMENT = '1SF5eAEj_yD-_pbb2Oc_UHoIWqgMrk5cDv_YRfF7134Q',
    TEAMWORKINGCOVER_DOCUMENT = '1ZWlRuzVDc33xFOEGOoeUjpzIQrKFrX7tB-eqyZcMdk0';

const MAINFILENAME_STRING = 'Caderno de Engenharia';

function main() {
    underAnalysisFilesToFormatted();
    generateEngineeringNotebook();
    generateUnderAnalysisFiles();
}

function underAnalysisFilesToFormatted() {
    // Coleta todos os arquivos da pasta "Em análise"
    // Envia-os para outra pasta "Formatados"
    // Deleta todos os arquivos da pasta "Em análise"
    const underAnalysisFiles = DriveApp.getFolderById(EMANALISE_FOLDER).getFiles()
    while (underAnalysisFiles.hasNext()) {
        const underAnalysisFile = underAnalysisFiles.next();
        if (underAnalysisFile.getMimeType() === "application/vnd.google-apps.document")
            underAnalysisFile.moveTo(DriveApp.getFolderById(FORMATADO_FOLDER));
    }
}

function generateEngineeringNotebook() {
    const generattedFolder = DriveApp.getFolderById(GERADO_FOLDER);
    const generattedFiles = generattedFolder.getFilesByName(MAINFILENAME_STRING);
    // Delete every Google Document inside "GERADO FOLDER"
    while (generattedFiles.hasNext()) {
        const generattedFile = generattedFiles.next();
        if (generattedFile.getMimeType() === "application/vnd.google-apps.document")
            generattedFile.setTrashed(true);
    }

    // Creates new file to use as Main File (copy from parent)
    const createdDoc = DriveApp.getFileById(PARENTFILE_DOCUMENT)
        .makeCopy(MAINFILENAME_STRING, generattedFolder);

    const body = DocumentApp.openById(createdDoc.getId()).getBody();
    body.appendPageBreak();

    const formattedFiles = DriveApp.getFolderById(FORMATADO_FOLDER).getFiles();

    const engineeringFiles = [],
        businessFiles = [],
        teamWorkFiles = [];

    while (formattedFiles.hasNext()) {
        const underAnalysisFile = formattedFiles.next();
        const fileName = underAnalysisFile.getName();
        const fileArea = fileName.substring(
            fileName.indexOf("[", 1) + 2, fileName.indexOf("]", 1)
        );

        // Cada área em sua respectiva lista
        const areaNameToList = {
            'Trabalho em equipe': teamWorkFiles,
            'Plano de Negócios': businessFiles,
            'Engenharia': engineeringFiles,
        };

        areaNameToList[fileArea].push(underAnalysisFile);
    }

    // Adiciona o conteúdo de "File" para o "body" do template
    // File -> https://developers.google.com/apps-script/reference/drive/file
    // Body -> https://developers.google.com/apps-script/reference/document/body
    function AppendToMainFile(body, file) {
        if (file.getMimeType() !== "application/vnd.google-apps.document")
            return;

        const otherBody = DocumentApp.openById(file.getId()).getActiveSection();
        const totalElements = otherBody.getNumChildren();
      for (let j = 0; j < totalElements; ++j)  {
            const element = otherBody.getChild(j).copy();
            const type = element.getType();
          
          if (type == DocumentApp.ElementType.PARAGRAPH) 
            body.appendParagraph(element);
            else if (type === DocumentApp.ElementType.TABLE)
                body.appendTable(element);
            else if (type === DocumentApp.ElementType.INLINE_IMAGE)
                body.appendImage(element);
            else if (type === DocumentApp.ElementType.LIST_ITEM)
                body.appendListItem(element);
            else
                throw new Error("Unknown element type: " + type);
        }
      
        body.appendPageBreak();
    }

    // Capa do Trabalho em Equipe
    AppendToMainFile(body, DriveApp.getFileById(TEAMWORKINGCOVER_DOCUMENT));
    // Adiciona todas as páginas de trabalho em equipe
    teamWorkFiles.map(file => {
        AppendToMainFile(body, file)
    });

    // Capa de Plano de Negócios
    AppendToMainFile(body, DriveApp.getFileById(BUSINESSPLANCOVER_DOCUMENT));
    // Adiciona todas as páginas de Plano de Negócios
    businessFiles.map(file => {
        AppendToMainFile(body, file)
    });

    // Capa de Engenharia
    AppendToMainFile(body, DriveApp.getFileById(ENGINEERINGCOVER_DOCUMENT));
    // Adiciona todas as páginas de Engenharia
    engineeringFiles.map(file => {
        AppendToMainFile(body, file)
    });

    // Remove blank pages
}

function generateUnderAnalysisFiles() {
    // Coleta todos os dados que estão com STATUS em branco
    // Gera arquivos para cada dia na pasta "Em análise"
    // usando o template definido
    // Seta o dia como "Em análise"
    const spreadSheet = SpreadsheetApp.openById(DATABASE_SHEET);
    const sheet = spreadSheet.getSheets()[0];
    const range = sheet.getDataRange();
    const values = range.getValues();

    // Para cada linha do banco de dados...
    for (let i = 1; i < values.length; i++) {

        const [created_at, area, date, time, author, participants, title, description, images, hashtags, what1, why1, when1, what2, why2, when2, what3, why3, when3, status] = values[i];

        const textReplacementsToDo = [
            ['«DATA»', date],
            ['«HORARIO»', time],
            ['«AUTOR»', author],
            ['«PARTICIPANTES»', participants],
            ['«ASSUNTO»', title],
            ['«DESCRICAO»', description],
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
        ];

        if (status === "EM ANÁLISE") {
            range.getCell(i + 1, 20).setValue('FORMATADO');
            continue;
        } else if (status === "FORMATADO")
            continue;

        const cell = range.getCell(i + 1, 20);
        cell.setValue('EM ANÁLISE');

        const areaNameToTemplateID = {
            'Engenharia': TEMPLATE_ENGINEERING,
            'Trabalho em equipe': TEMPLATE_TEAMWORK,
            'Plano de Negócios': TEMPLATE_BUSINESSPLAN
        };

        Logger.log(area)

        const createdFile = DriveApp.getFileById(areaNameToTemplateID[area])
            .makeCopy('null', DriveApp.getFolderById(EMANALISE_FOLDER));
        const fileName = '[' + area + '] ' + date + ' | ' + title;

        // Rename
        DriveApp.getFileById(createdFile.getId()).setName(fileName);

        const createdDocument = DocumentApp.openById(createdFile.getId());

        textReplacementsToDo.map(replacement => {
            createdDocument.getBody().replaceText(replacement[0], replacement[1]);
        });

        const replaceTextToImage = (body, searchText, image, height) => {
            const text = body.findText(searchText);
            if (text === null)
             return;
          
            const r = text.getElement();
          
            r.asText().setText("");
            const img = r.getParent().asParagraph().insertInlineImage(0, image);
            if (height && typeof height == "number") {
                const w = img.getWidth();
                const h = img.getHeight();
                img.setWidth(height * w / h);
                img.setHeight(height);
            }
        };

        const replaceText = "«IMAGENS»";
        images.split(',').map(imgDriveURL => {
            const image = DriveApp.getFileById(imgDriveURL.split('?id=')[1]).getBlob();
            replaceTextToImage(createdDocument.getBody(), replaceText, image, 200);
        })

        // TODO: BACKUP

    }
}

/**
 * Get column index by given a name as String
 * @param  {String} columnName Which column name should use to search
 * @param  {String} sheetID ID of Google Spreadsheet like xxxxxxxxxxxxxxxxxxxxxxxxxxxx
 * @param  {Number} sheetIndex Sheet index to use as reference. Default is zero (0)
 * @return {String} index of column with the given name
 */
function getColumnIndexByName(columnName, sheetID, sheetIndex = 0) {
    const sheet = SpreadsheetApp.openById(sheetID).getSheets()[sheetIndex].getDataRange().getValues();
    return sheet[0].indexOf(columnName);
}

function onOpen() {
    SpreadsheetApp.getUi()
        .createMenu('CE Auto')
        .addItem('Gerar Caderno de Engenharia', 'main')
        .addToUi();
}