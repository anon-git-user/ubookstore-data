import scraperwiki
import requests

def getOptions(url):
    optionsRaw = requests.get(url)
    optionsDict = optionsRaw.json()['adoptionSearchParam']['Options']
    return optionsDict

def getBooks(url):
    bookRaw = requests.get(url)
    bookDict = bookRaw.json()
    return bookDict

def makeURL(schoolID='', termID='', departmentID='', catalogNmbr=''):
    catalogNmbr = catalogNmbr.replace("&", "%26")
    catalogNmbr = catalogNmbr.replace(" ", "+")
    urlRet= "https://www.ubookstore.com/ubs-vinson/services/AdoptionSearch.Service.ss?c=4487126&school=%s&term=%s&department=%s&catalogNmbr=%s&isAllowed=true&n=2&searchAdoptionParameters=true" % (schoolID, termID, departmentID, catalogNmbr)
    return urlRet

idKey = 0

for school in getOptions(makeURL()):
    for term in getOptions(makeURL(school['id'])):
        for department in getOptions(makeURL(school['id'], term['id'])):
            for course in getOptions(makeURL(school['id'], term['id'], department['id'])):
                for section in getOptions(makeURL(school['id'], term['id'], department['id'], course['id'])):
                    bookURL = "https://www.ubookstore.com/ubs-vinson/services/AdoptionSearch.Service.ss?c=4487126&ccId=%s&n=2&searchAdoptions=true" % section['id']
                    # print(bookURL)
                    for book in getBooks(bookURL):
                        # print(book['items'])
                        if isinstance(book['items'], list):
                            for item in book['items']:
                                idKey += 1 
                                if item['isbn']=="9780000000002":
                                    item['isbn'] = "No Text Required"

                                scraperwiki.sqlite.save(
                                    unique_keys=['id'], data={ 
                                        "id": idKey, 
                                        "schoolName": school['name'],
                                        "termName": term['name'], 
                                        "departmentName": department['name'], 
                                        "courseName": course['name'], 
                                        "sectionName": section['name'],
                                        "isbn": item['isbn'],
                                        "title": item['longTitle'],
                                        "author": item['bookAuthor'],
                                        "edition": item['bookEdition'],
                                        "required": item['courseMaterialRequirement'],
                                        "substituteOK": str(item['okToSubstitute']),
                                        "sectionNotes": item['sectionNotes']
                                        })

                        # else:
                        #     idKey += 1 
                        #     print(str(idKey), school['name'], term['name'], department['name'], course['name'], section['name'], "Text Status Unknown", sep=',  ')


