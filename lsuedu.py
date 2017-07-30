import requests
import string

from bs4 import BeautifulSoup

baseLink = 'http://cth.uca.es'

totalPages = 3

count = 0

separator = ','

f = open("lsuedu.csv", "wb")

f.write('Title, articleCode, Date,  Author, Description\n')

for pageNum in range(1,totalPages):

    url = baseLink+"/eng/patents/cartera-patentes/"+str(pageNum)

    r  = requests.get(url)

    data = r.text

    soup = BeautifulSoup(data,"html.parser")

    columanchaizq = soup.find("div", { "class" : "columanchaizq" })
    paragraphs = columanchaizq.find_all("p")
    h4s = columanchaizq.find_all("h4")

    # print(h4)

    for index, paragraph in enumerate(paragraphs[1:]):

        print(index)
        h4 = h4s[index]
        title = h4.find("a").string
        title = title.replace(",", "")
        title = title.replace("'", "")
        title = title.replace('"', "")
        title = title.replace("\n", "")
        title = title.replace("\r", "")
        f.write(title.encode('utf8')+separator)

        detail_link = paragraph.a.get("href")
        # detail_url = baseLink+'/eng/patents/cartera-patentes/2/novel-synthesis-procedure-of-gold-nanoparticles'
        detail_url = baseLink+detail_link
        detailPages = requests.get(detail_url)
        detailData = detailPages.text
        detailSoup = BeautifulSoup(detailData,"html.parser")

        subtit = detailSoup.find("p", {"class": "subtit"})
        articleCodeElement = subtit.strong

        if articleCodeElement == None:
            articleCode = "Unknown Code"
        else:
            articleCode = articleCodeElement.string

        f.write(articleCode+separator)

        dateElement = subtit.find("span", {"class": "fecha"})

        if dateElement == None:
            date = "Unknown"
        else:
            date = dateElement.string

        f.write(date+separator)
        # author capturing
        columanchaizq = detailSoup.find("div", { "class": "columanchaizq" } )
        columanchaizqAllPs = columanchaizq.find_all("p")
        authorElement = columanchaizqAllPs[2].find("strong")

        if authorElement == None:
            author = "Unknown"
        else:
            author = authorElement.string

        author = author.replace(",", "; ")
        author = author.replace("'", "")
        author = author.replace('"', "")
        author = author.replace("\n", "")
        author = author.replace("\r", "")
        f.write(author.encode('utf8')+separator)


        #intro capturing with class "resumen"

        resumen = detailSoup.find("div", {"class": "resumen"})
        if resumen:
            resumenAllPs = resumen.find("p")
            intro = resumenAllPs.text
        else:
            intro ="Description not available..."




        intro = intro.replace(",", "")
        intro = intro.replace("'", "")
        intro = intro.replace('"', "")
        intro = intro.replace("\n", "")
        intro = intro.replace("\r", "")

        f.write(intro.encode('utf8')+'\n')
        # f.write(desc.encode('utf8')+'\n')

f.close()

'''
f = open("datacenters.txt", "wb")

for provider in providers:
    providerName = provider.span.text+"\n"
    f.write(providerName.encode('utf8'))

f.close()
'''

quit()



