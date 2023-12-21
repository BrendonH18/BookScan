import cv2
from pyzbar.pyzbar import decode
import requests as requests1
import json
from openpyxl.workbook import Workbook

from handlers.handlers import google_process_elements, openLibrary_process_elements


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def isValidISBN(number):
    lenth = len(number)
    if lenth == 13:
        total = 0
        for index, number in enumerate(number[::-1]):
            if (index + 1) % 2 == 0:
                factor = 3
            else:
                factor = 1
            sum = factor * int(number)
            total = total + sum
        if total % 10 == 0:
            return True
        return False
    if len(number) == 10:
        total = 0
        for index, number in enumerate(number[::-1]):
            sum = (index + 1) * int(number)
            total = total + sum
        if total % 11 == 0:
            return True
        return False
    return False

screen = cv2.VideoCapture(0)
screen.set(3, 640)
screen.set(4,480)
isCapture = True
while isCapture == True:
    success, frame = screen.read()
    isDecodeFrameComplete = False
    decodeFrame = None
    while not isDecodeFrameComplete:
        try:
            decodeFrame = decode(frame)
            isDecodeFrameComplete = True
        except:
            continue
    for code in decodeFrame:
        # print(code.type)
        code_number=code.data.decode('utf-8')
        # print(code.data.decode('utf-8'))
        if isValidISBN(code_number) == True:
            output = {
                'authors': 'PENDING',
                'subjects': 'PENDING',
                'pages': 'PENDING',
                'description': 'PENDING',
                'language': 'PENDING',
                'thumbnail': 'PENDING',
                'title': 'PENDING',
                'isbn': int(code_number)
            }

            with requests1.get(f"https://openlibrary.org/isbn/{code_number}.json") as openlibrary_raw:
                if openlibrary_raw.status_code == 200:
                    openLibrary_process_elements(json.loads(openlibrary_raw.text), output)

            with requests1.get("https://www.googleapis.com/books/v1/volumes?q=isbn:" + code_number) as google_raw:
                if google_raw.status_code == 200:
                    if not json.loads(google_raw.text)['totalItems'] == 0:
                        google_process_elements(json.loads(google_raw.text)['items'][0]['volumeInfo'], output)


            
            # If modifying these scopes, delete the file token.json.
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

            # The ID and range of a sample spreadsheet.
            SAMPLE_SPREADSHEET_ID = "1KLO6qfvfxpfUfUE-iEBdVVOaD6GgtzGeAKtKUwsHsr0"
            SAMPLE_RANGE_NAME = "'From Scan'!a1:h1"
            SAMPLE_SHEET_ID = "434979763"

            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())

            try:
                service = build("sheets", "v4", credentials=creds)
                values = [
                    [output['title'], output['authors'], output['subjects'], output['language'], output['pages'], output['isbn'], output['description'], output['thumbnail']],
                ]
                body = {
                    'values': values
                }





                # Call the Sheets API
                sheet = service.spreadsheets()
                result = (
                    sheet.values()
                    .append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED", body=body)
                    # .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
                    .execute()
                )
            except HttpError as err:
                print(err)

            pass
        print(".")
        

    cv2.imshow('Testing-code-scan', frame)
    cv2.waitKey(1)

# while True:
#     main()