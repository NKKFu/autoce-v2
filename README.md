# Auto C.E. v2

Auto C.E. is a python program used in the First Tech Challenge as a tool for organizing the engineering notebook in an online, automatic and integrating way with Google services. Code developed with the purpose of helping other teams to have more organization in engineering notebooks online.

Thanks for seeing my repository, I appreciate that:)

## How it works

Our python program integrates with Google Docs, Drive and Sheets API to request some data from its sources.

First, we collect all data avaliable in the main database source `DATABASE_SHEET` inside the Google Spreadsheet based on the columns `DATABASE_FIELDS_REPRESENTATION` of the first sheet.

First, we collect all the data available from the main source of the database `DATABASE_SHEET` within Google Spreadsheet based on the `DATABASE_FIELDS_REPRESENTATION` columns in the first spreadsheet.

> We back up the database, just to ensure that we don't lose data. But we ** can't change anything in the database, just read **

Based on this information, we generate many files using a copy of the template files `TEMPLATE_FILES_ID` and replacing each specified field` DATABASE_FIELDS_REPRESENTATION` with its correspondent in the database _(based on the order, therefore the order in the database fields and in config.json is important to us)_

> **THE FIRST THREE DATABASE COLUMNS MUST BE: CREATED_AT, AREA, DATE**, but the names don't matter, just the order of those elements.

After generating these files, we put them in a specific Google Drive folder `DEFAULT_FOLDER`, and then we download them in PDF format on our computer _(just to make a backup of the files)_

## Requirements

- One account from Google (@gmail.com)
    - You **don't** need have a Google Developer's Account
- Python 3.7.x and pip installed on your machine (3.7.3 is recommended)
    - Install it from [Python](python.org)
- This repository installed on your computer
- Follow steps on next session

## Steps to get started

- Clone this repository to your computer [How?](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)
- Log-in on Google Cloud Plataform [Here](https://cloud.google.com/?hl=en)
- Enter on GCP's Console [Here](https://console.cloud.google.com/)
- Create a project by clicking _"Select project > NEW PROJECT"_
    - _(This can be found on top left border of screen)_
- Select your recently created project by clicking _"Select project"_
- Enable Google Drive API, Google Docs API, Google Sheets API
    - _(Just cick "Enable" for each link below)_
    - [Google Docs API](https://console.cloud.google.com/marketplace/product/google/docs.googleapis.com)
    - [Google Sheets API](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com)
    - [Google Drive API](https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com)
- On Google Drive API, go to _"Credentials > + CREATE CREDENTIALS"_ (middle-left border)
- Select _"OAuth client ID"_
- Select _"CONFIGURE CONSENT SCREEN > External > Create"_
    - **By selecting this options, your app will be public, but don't worry, your credentials don't will until you protect them**
- Follow steps from Google (information about your app)
    - _Skip "Scopes" section, we'll configure that later_
- After that, go back to _"Credentials > + CREATE CREDENTIALS > OAuth client ID"_ (middle-left border)
- For an application type, select _"Desktop App"_
- Put a name on your new credential and create it
- Click on your recently generated credentials
- Click _"Download JSON"_ on the top of your screen
- Rename it to credentials.json
- Download python library required for this project by executig this commands:
    - `pip install -r requirements.txt` or `pip3 install -r requirements.txt`
- Open file example_config.json
    - Rename it to config.json 
    - Change some fields based on your configuration setup
- Execute this on your command line:
    - `python autoce.py` or `python3 autoce.py`

## License and credits

This project was idealized and partially developed by Nelson Kenmochi, a member from Team ProdiXy # 16050 from Brazil. It uses MIT license, feel free to use, modify and collaborate as you want without hurt it's license.