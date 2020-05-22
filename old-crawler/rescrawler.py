
# bothell
#   school = 2
#   fall = 255
#   winter = 270
#  
# cc 
#   school = 4
#   fall = 249
#   winter = 269


import urllib.request, json
school = "4"
term = "269"
usefile = True
outfile = open('bookOutput.csv', 'w')
deptUrl = "https://www.ubookstore.com/ubs-vinson/services/AdoptionSearch.Service.ss?c=4487126&catalogNmbr=&department=&isAllowed=true&n=2&school="+school+"&searchAdoptionParameters=true&term="+term
with urllib.request.urlopen(deptUrl) as url:
    departmentdata = json.loads(url.read().decode())
    for department in departmentdata['adoptionSearchParam']['Options']:
        courseurl = "https://www.ubookstore.com/ubs-vinson/services/AdoptionSearch.Service.ss?c=4487126&catalogNmbr=&department="+department['id']+"&isAllowed=true&n=2&school="+school+"&searchAdoptionParameters=true&term="+term
        with urllib.request.urlopen(courseurl) as url:
            coursedata = json.loads(url.read().decode())
            for catalogNmbrData in coursedata['adoptionSearchParam']['Options']:
                catStr = (catalogNmbrData['id'].replace(" ","+"))
                catNmbrUrl = "https://www.ubookstore.com/ubs-vinson/services/AdoptionSearch.Service.ss?c=4487126&catalogNmbr="+catStr+"&department="+department['id']+"&isAllowed=true&n=2&school="+school+"&searchAdoptionParameters=true&term="+term
                with urllib.request.urlopen(catNmbrUrl) as url:
                    sectionData = json.loads(url.read().decode())
                    for section in sectionData['adoptionSearchParam']['Options']:
                        sectionBookUrl = "https://www.ubookstore.com/ubs-vinson/services/AdoptionSearch.Service.ss?c=4487126&ccId="+section["id"]+"&n=2&searchAdoptions=true"
                        with urllib.request.urlopen(sectionBookUrl) as url:
                            bookData = json.loads(url.read().decode())
                            for book in bookData:
                                if isinstance(book['items'], list):
                                    bookList = book['items']                                    
                                    for item in bookList:
                                        line = section["name"]
                                        if item['isbn']=="9780000000002":
                                            line = section["name"] + "; No Text Required"
                                            print ( line )
                                            if usefile: print ( line, file=outfile )
                                        else:
                                            line = section["name"]
                                            line = line + "; "+ item['isbn'] 
                                            line = line + "; "+ item['longTitle'] 
                                            line = line + "; "+ item['bookAuthor']
                                            line = line + "; "+ item['bookEdition']
                                            line = line + "; "+ item['courseMaterialRequirement']
                                            line = line + "; "+ str(item['okToSubstitute'])
                                            line = line + "; "+ item['sectionNotes']
                                            print ( line)
                                            if usefile: print ( line, file=outfile )
                                else:
                                    line = section["name"] + "; Text Status Unknown"
                                    print ( line )
                                    if usefile: print ( line, file=outfile )

outfile.close
