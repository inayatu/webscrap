import requests
import string

from bs4 import BeautifulSoup

baseLink = 'http://otd.harvard.edu'

totalPages = 3

count = 0

separator = ','

f = open("harvard.csv", "wb")

f.write('Research Title, Summary, Author\n')

url = baseLink+"/explore-innovation/technologies"

r  = requests.get(url)

data = r.text

soup = BeautifulSoup(data,"html.parser")

mainCategory = soup.find("div", { "class" : "category-columns-container" })

ulCol = mainCategory.find_all("ul")
print('length of ulCol', len(ulCol))

for ulIndex in range(0, len(ulCol)):
    fondCol = ulCol[ulIndex].find_all("li")
    print('ulCol+ulIndex: %d', len(fondCol))

    for liIndex in range(0, len(fondCol)):
        newUrl = fondCol[liIndex].a.get("href")
        newUrl = baseLink+newUrl
        print('newUrl:', newUrl )

        # Go to new page and fetch data 
        searchResultPage = requests.get(newUrl)
        searchResultPageData = searchResultPage.text
        searchResultPageSoup = BeautifulSoup(searchResultPageData,"html.parser")

        searchedLi = searchResultPageSoup.find_all("li", {"class" : "search-result-item"})

        # (pagination) get all the uls and lis of 3 other pages
        page2Url = "http://otd.harvard.edu/explore-innovation/technologies/results/search&keywords=&category=Computer+Science/Bioinformatics/P10/"
        page3Url = "http://otd.harvard.edu/explore-innovation/technologies/results/search&keywords=&category=Computer+Science/Bioinformatics/P20/"

        page2Result = requests.get(page2Url)
        page2Result = page2Result.text
        page2Result = BeautifulSoup(page2Result,"html.parser")
        page2Result = page2Result.find_all("li", {"class" : "search-result-item"})
        print('page2Result:', len(page2Result))

        page3Result = requests.get(page3Url)
        page3Result = page3Result.text
        page3Result = BeautifulSoup(page3Result,"html.parser")
        page3Result = page3Result.find_all("li", {"class" : "search-result-item"})
        print('page3Result:', len(page3Result))


        searchedLi = searchedLi+page2Result+page3Result

        print('Length of searchedLi:', len(searchedLi))

        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        
        print('searchedLi::', searchedLi)

        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

        # print('Sum of Page results:', len(searchedLi)+len(page2Result)+len(page3Result)
        # print('lenght of searchedLi:', searchedLi)

        # Find all urls in lists and go to those pages
        for searchedIndex in range(0, len(searchedLi)):
            # findDetail = searchedLi[searchedIndex].find("li")
            detailedUrl = searchedLi[searchedIndex].a.get("href")
            detailedUrl = baseLink+detailedUrl
            print('detailedUrl:', detailedUrl)

            # Find title and description 
            detailPage = requests.get(detailedUrl)
            detailPageData = detailPage.text
            detailPageDataSoup = BeautifulSoup(detailPageData,"html.parser")

            article = detailPageDataSoup.find("article", {"class" :"content-main"})

            if not article:
                print('Khaali H2')
            else:
                title = article.find("h2")
                title = title.string
                print("Title:", title)
                title = title.replace(",", "")
                title = title.replace("'", "")
                title = title.replace('"', "")
                title = title.replace("\n", "")
                title = title.replace("\r", "")
                f.write(title.encode('utf8')+separator)
                # For summary find all p except last one
                summary = article.find_all("p")
                sumLen = len(summary)
                fullSum = ""
                for pIndex in range(0, sumLen):
                    fullSum = fullSum + summary[pIndex].text
                
                print("summary:", fullSum)
                fullSum = fullSum.replace(",", "")
                fullSum = fullSum.replace("'", "")
                fullSum = fullSum.replace('"', "")
                fullSum = fullSum.replace("\n", "")
                fullSum = fullSum.replace("\r", "")
                f.write(fullSum.encode('utf8')+separator)

                fullSum = ""

            # for author name
            authorDiv = detailPageDataSoup.find_all("h4", {"class" :"team-name"});
            print('authorDiv:::',authorDiv)
            if not authorDiv:
                author = "Unknown/Group of People"                
                f.write(author.encode('utf8')+"\n")
                print('khaaali', author)
            else:
                author = detailPageDataSoup.find_all("h4", {"class" :"team-name"})[0].a.text
                print("Author:::", author)
                author = author.replace(",", "")
                author = author.replace("'", "")
                author = author.replace('"', "")
                author = author.replace("\n", "")
                author = author.replace("\r", "")
                f.write(author.encode('utf8')+"\n")

            
f.close()

quit()