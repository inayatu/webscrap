import requests
import string

from bs4 import BeautifulSoup

baseLink = "http://lahann.engin.umich.edu/research"

separator = ','

f = open("lahann.csv", "wb")
f.write("Research Title, Background, Technology and Advantages over Naturally-Derived Matrices, Application\n")

url = baseLink
r = requests.get(url)
data = r.text

soup = BeautifulSoup(data,"html.parser")

result = soup.find("td", {"class" : "sites-layout-tile"})
links = result.find_all("a")

length = len(links)-4

for index in range(0, length):
    if(index == 1):
        title = soup.find("font").text
        print('Mai khali hun', title)
    else:
        title = links[index].text
        newUrl = links[index].get("href")
        print('Link text:',title)
        print('Link is:',newUrl)

        title = title.replace(",", " ")
        title = title.replace("'", " ")
        title = title.replace('"', " ")
        title = title.replace("\n", " ")
        title = title.replace("\r", " ")
        title = title.replace("\t", " ")

        # get data from new url
        urlData = requests.get(newUrl).text
        urlSoup = BeautifulSoup(urlData, "html.parser")

        backgr = urlSoup.find("div", {"class" : "sites-tile-name-header"})
        techAdvan = urlSoup.find("td", {"class" : "sites-tile-name-content-1"})
        application = urlSoup.find("div", {"class" : "sites-tile-name-footer"})
        application = application.find_all("font")

        # tech = 
        backgr = backgr.text
        techAdvan = techAdvan.text
        application = application[1].text

        backgr = backgr.replace(",", " ")
        backgr = backgr.replace("'", " ")
        backgr = backgr.replace('"', " ")
        backgr = backgr.replace("\n", " ")
        backgr = backgr.replace("\r", " ")
        backgr = backgr.replace("\t", " ")

        techAdvan = techAdvan.replace("'", " ")
        techAdvan = techAdvan.replace('"', " ")
        techAdvan = techAdvan.replace("\n", " ")
        techAdvan = techAdvan.replace("\r", " ")
        techAdvan = techAdvan.replace("\t", " ")

        application = application.replace(",", " ")
        application = application.replace("'", " ")
        application = application.replace('"', " ")
        application = application.replace("\n", " ")
        application = application.replace("\r", " ")
        application = application.replace("\t", " ")

        f.write(title.encode('utf8')+separator)
        f.write(backgr.encode('utf8')+separator)
        f.write(techAdvan.encode('utf8')+separator)
        f.write(application.encode('utf8'+"\n"))

        print('___________________________________________________________')
        print('Background::', backgr)
        print('___________________________________________________________')

        print('techAdvan::', techAdvan)
        print('___________________________________________________________')

        print('application::', application)
        print('___________________________________________________________')


# URl of third link
url3 = baseLink+"/atrp"
url3 = requests.get(url3)
data3 = url3.text

soup3 = BeautifulSoup(data3,"html.parser")
title = soup3.find("span", {"id" : "sites-page-title"}).text
title = title.replace(",", " ")
title = title.replace("'", " ")
title = title.replace('"', " ")
title = title.replace("\n", " ")
title = title.replace("\r", " ")
title = title.replace("\t", " ")


backgr = soup3.find("div", {"class" : "sites-tile-name-header"})
techAdvan = soup3.find("td", {"class" : "sites-tile-name-content-1"})
application = soup3.find("div", {"class" : "sites-tile-name-footer"})
application = application.find_all("font")


backgr = backgr.text
techAdvan = techAdvan.text
application = application[1].text

backgr = backgr.replace(",", " ")
backgr = backgr.replace("'", " ")
backgr = backgr.replace('"', " ")
backgr = backgr.replace("\n", " ")
backgr = backgr.replace("\r", " ")
backgr = backgr.replace("\t", " ")

techAdvan = techAdvan.replace("'", " ")
techAdvan = techAdvan.replace('"', " ")
techAdvan = techAdvan.replace("\n", " ")
techAdvan = techAdvan.replace("\r", " ")
techAdvan = techAdvan.replace("\t", " ")

application = application.replace(",", " ")
application = application.replace("'", " ")
application = application.replace('"', " ")
application = application.replace("\n", " ")
application = application.replace("\r", " ")
application = application.replace("\t", " ")

print('background::', backgr)
print('techAdvan::', techAdvan)


f.write(title.encode('utf8')+separator)
f.write(backgr.encode('utf8')+separator)
f.write(techAdvan.encode('utf8')+separator)


f.close
quit()