import requests as requests1
import json

def openLibrary_extract_title(openLibrary, output):
    output['title'] = openLibrary['title']
def openLibrary_extract_authors(openLibrary, output):
    authors = ""
    count = 0
    for author in enumerate(openLibrary["authors"]):
        for auth in author:
            if type(auth) is dict:
                author_raw = requests1.get(f'https://openlibrary.org'+auth['key']+".json")
                author_obj = json.loads(author_raw.text)
                if count == 0:
                    authors = author_obj["name"]
                    count += 1
                    continue
                authors = authors + ", " + author_obj["name"]
                count += 1
    output['authors'] = authors
def openLibrary_extract_subjects(openLibrary, output):
    subjects = ", ".join(openLibrary['subjects'])
    # subjects = ""
    # for index, subject in enumerate(openlibrary_dict["subjects"]):
    #     if index == 0:
    #         subjects = subject
    #         continue
    #     subjects = subjects + ", " + subject
    output['subjects'] = subjects
def openLibrary_extract_pages(openLibrary, output):
    output['pages'] = openLibrary["number_of_pages"]
def openLibrary_extract_description(openLibrary, output):
    output['description'] = openLibrary['description']['value']
def openLibrary_process_elements(openLibrary, output):
    if 'title' in openLibrary and output['title'] == "PENDING":
        openLibrary_extract_title(openLibrary, output)
    if "authors" in openLibrary and output['authors'] == "PENDING":
        openLibrary_extract_authors(openLibrary, output)
    if "subjects" in openLibrary and output['subjects'] == "PENDING":
        openLibrary_extract_subjects(openLibrary, output)
    if 'number_of_pages' in openLibrary and output['pages'] == "PENDING":
        openLibrary_extract_pages(openLibrary, output)
    if 'description' in openLibrary and output['description'] == "PENDING":
        openLibrary_extract_description(openLibrary, output)



def google_extract_authors(google, output):
    authors = ", ".join(google['authors'])
    # authors = ''
    # for index, author in enumerate(google_dict['authors']):
    #     if index == 0:
    #         authors = author
    #         continue
    #     authors = authors + ', ' + author
    output['authors'] = authors
def google_extract_title(google, output):
    output['title'] = google['title']
def google_extract_pages(google, output):
    output["pages"] = google['pageCount']
def google_extract_description(google, output):
    output['description'] = google['description']
def google_extract_language(google, output):
    language_lib = {
        'en': "Inglés",
        'es': "Español"
    }
    if google['language'] in language_lib:
        output['language'] = language_lib[google['language']]
        return 
    output['language'] = google['language']
def google_extract_thumbnail(google, output):
    if 'thumbnail' in google['imageLinks']:
        thumbnail = google['imageLinks']['thumbnail']
        output['thumbnail'] = thumbnail
def google_process_elements(google, output):
    if 'authors' in google and output['authors'] == 'PENDING':
        google_extract_authors(google, output)
    if 'title' in google and output['title'] == 'PENDING':
        google_extract_title(google,output)
    if 'pageCount' in google and output['pages'] == "PENDING":
        google_extract_pages(google, output)
    if 'description' in google and output['description'] == 'PENDING':
        google_extract_description(google, output)
    if 'language' in google and output['language'] == "PENDING":
        google_extract_language(google, output)
    if 'imageLinks' in google and len(google["imageLinks"])>0 and output['thumbnail'] == "PENDING":
        google_extract_thumbnail(google, output)