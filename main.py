import cv2
from pyzbar.pyzbar import decode
import requests as requests1
import json
from openpyxl.workbook import Workbook

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
    for code in decode(frame):
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
            openlibrary_raw = requests1.get(f"https://openlibrary.org/isbn/{code_number}.json")
            if openlibrary_raw.status_code == 200:    
                openlibrary_dict = json.loads(openlibrary_raw.text)

                if 'title' in openlibrary_dict:
                    output['title'] = openlibrary_dict['title']

                if "authors" in openlibrary_dict:
                    authors = ""
                    count = 0
                    for author in enumerate(openlibrary_dict["authors"]):
                        for auth in author:
                            if type(auth) is dict:
                                author_raw = requests.get(f'https://openlibrary.org'+auth['key']+".json")
                                author_obj = json.loads(author_raw.text)
                                if count == 0:
                                    authors = author_obj["name"]
                                    continue
                                authors = authors + ", " + author_obj["name"]
                    
                    output['authors'] = authors

                
                if "subjects" in openlibrary_dict:
                    subjects = ""
                    for index, subject in enumerate(openlibrary_dict["subjects"]):
                        if index == 0:
                            subjects = subject
                            continue
                        subjects = subjects + ", " + subject
                    output['subjects'] = subjects

                if 'number_of_pages' in openlibrary_dict:
                    pages = openlibrary_dict["number_of_pages"]
                    output['pages'] = pages

                if 'description' in openlibrary_dict:
                    description = openlibrary_dict['description']['value']
                    output['description'] = description

            google_raw = requests1.get("https://www.googleapis.com/books/v1/volumes?q=isbn:" + code_number)
            
            if google_raw.status_code == 200:    
                google_dict = json.loads(google_raw.text)['items'][0]['volumeInfo']

                if 'authors' in google_dict and output['authors'] == 'PENDING':
                    authors = ''
                    for index, author in enumerate(google_dict['authors']):
                        if index == 0:
                            authors = author
                            continue
                        authors = authors + ', ' + author
                    output['authors'] = authors

                if 'title' in google_dict and output['title'] == 'PENDING':
                    output['title'] = google_dict['title']

                if 'pageCount' in google_dict and output['pages'] == "PENDING":
                    output["pages"] = google_dict['pageCount']

                if 'description' in google_dict and output['description'] == 'PENDING':
                    output['description'] = google_dict['description']
                
                if 'language' in google_dict:
                    language = google_dict['language']
                    output['language'] = language

                if 'imageLinks' in google_dict and len(google_dict["imageLinks"])>0:
                    if 'thumbnail' in google_dict['imageLinks']:
                        thumbnail = google_dict['imageLinks']['thumbnail']
                        output['thumbnail'] = thumbnail

            headers = ['Title', 'Authors', 'Pages', 'Language', 'Subjects', 'ISBN', 'Description', 'thumbnail']
            print("Hello")


            pass
        print(".")
        

    cv2.imshow('Testing-code-scan', frame)
    cv2.waitKey(1)

# while True:
#     main()