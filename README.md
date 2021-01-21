# Auto C.E. v2

Auto C.E. is a python program used in the First Tech Challenge as a tool for organizing the engineering notebook in an online, automatic and integrating way with Google services. Code developed with the purpose of helping other teams to have more organization in engineering notebooks online.

Thanks for seeing my repository, I appreciate that:)

## How it works

- - -

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
> Need to change this steps, don't do the steps bellow
- Change file config.json
- Execute this on your command line:
    - `python autoce.py` or `python3 autoce.py`

## License and credits

This project was idealized and partially developed by Nelson Kenmochi, a member from Team ProdiXy # 16050 from Brazil. It uses MIT license, feel free to use, modify and collaborate as you want without hurt it's license.