import requests
import string

from bs4 import BeautifulSoup

baseLink = "http://www.tto.hku.hk"

separator = ','

f = open("tto.csv", "wb")
f.write("Title, department, Detail\n")
url = baseLink+"/technology/issued-patents"
r = requests.get(url)
data = r.text

soup = BeautifulSoup(data,"html.parser")
patentMajor = soup.find("div", {"class": "rich-middle"})
patentMajor = patentMajor.find_all("a")
# print("table is:::", patentMajor)

for i in range(0, len(patentMajor)):
	catName = patentMajor[i].find("img").get("alt")
	catUrl = patentMajor[i].get("href")
	catUrl = baseLink+catUrl
	print("cat:", catName)
	print("catUrl:", catUrl)

	# catName = catName.get_text(strip=True)
	catName = catName.replace(",", " ")
	catName = catName.replace("'", " ")
	catName = catName.replace('"', " ")
	catName = catName.replace("\n", " ")
	catName = catName.replace("\r", " ")
	catName = catName.replace("\t", " ")

	

	# find list from second page
	catData = requests.get(catUrl)
	catData = catData.text
	catSoup = BeautifulSoup(catData, "html.parser")

	sublinks = catSoup.find_all("div", {"class":"department"})
	for j in range(0, len(sublinks)):
		detailedLink = sublinks[j].find_all("a")
		detailedLink = detailedLink[1].get("href")

		detailUrl = baseLink+detailedLink
		print("Detailed Url::", detailUrl)

		# f.write(catName.encode('utf8')+separator)
		# f.write(detailUrl.encode('utf8')+separator)

		# Fetch detail from last page
		detail = requests.get(detailUrl)
		detail = detail.text
		detailSoup = BeautifulSoup(detail, "html.parser")
		detailData = detailSoup.find("div", {"class":"rich-middle"})
		deptName = detailData.find("h4").text

		pagination = detailData.find("div", {"class":"top"})
		pagination = pagination.find_all("a")
		print("print pagination::", len(pagination))

		if not pagination:
			print("With No Pagination")		
			
			page1 = detailData.find("ul", {"class":"project"})
			page1 = page1.find_all("li")
			newPage1 = ''
			for newIndex in range(0, len(page1)):
					newPage1 = newPage1+page1[newIndex].text
			print("page1", page1)
			# newPage1 = newPage1.get_text(strip=True)
			newPage1 = newPage1.replace(",", " ")
			newPage1 = newPage1.replace("'", " ")
			newPage1 = newPage1.replace('"', " ")
			newPage1 = newPage1.replace("\n", " ")
			newPage1 = newPage1.replace("\r", " ")
			newPage1 = newPage1.replace("\t", " ")

			print("last page list::", page1)

			f.write(catName.encode('utf8')+separator)
			f.write(deptName.encode('utf8')+separator)
			f.write(newPage1.encode('utf8')+separator)

		else:
			for k in range(0, len(pagination)):
				print("With Pagination")
				newPage = pagination[k]
				newPageUrl = newPage.get("href")
				newPageUrl = baseLink+newPageUrl
				print("New Pageeee:::", newPageUrl)

				newPg = requests.get(newPageUrl)
				newPgData = newPg.text
				soup = BeautifulSoup(newPgData, "html.parser")

				newData = soup.find("div", {"class":"rich-middle"})
				newData = newData.find("ul", {"class":"project"})
				newData = newData.find_all("li")

				newDetail = ''
				for newIndex in range(0, len(newData)):
					newDetail = newDetail+newData[newIndex].text

				# newPg = newPg.string
				# newDetail = newDetail.get_text(strip=True)
				newDetail = newDetail.replace(",", " ")
				newDetail = newDetail.replace("'", " ")
				newDetail = newDetail.replace('"', " ")
				newDetail = newDetail.replace("\n", " ")
				newDetail = newDetail.replace("\r", " ")
				newDetail = newDetail.replace("\t", " ")

				f.write(catName.encode('utf8')+separator)
				f.write(deptName.encode('utf8')+separator)
				f.write(newDetail.encode('utf8')+separator)
				f.write("\n")
		f.write("\n")

	# f.write("\n")
# pass
# print("Total Sublinks::", len(sublinks))

f.close
quit()