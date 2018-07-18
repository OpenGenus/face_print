from bs4 import BeautifulSoup as bs
import requests
import lxml
import os
import json
import os.path


def getimgurl(url):
	resp=requests.get(url)
	soup=bs(resp.text,'lxml')
	tag=soup.find("a",{"class":"image"})
	link=""
	if tag is not None:
	    link="https://en.wikipedia.org"+tag['href']
	    resp=requests.get(link)
	    soup=bs(resp.text,'lxml')
	    tag=soup.find("div",{"class":"fullImageLink"})
	    tag=tag.find("a")
	    if tag is not None:
	    	link="https:"+tag['href']
	    	return link
	return None

def tojson(fileopen,data):
	with open(fileopen,'w') as f:
		f.write("{\"index\":")
		json.dump(data,f,indent=2)
		f.write("}")


new_path=r'/home/tanmay/Documents/image_ogo/raw_data_winner'
os.makedirs(new_path)

filejson='raw_data_winner/image_mapping_winner.json'
index=[]

url="https://en.wikipedia.org/wiki/Category:Turing_Award_laureates"
req=requests.get(url)
soup=bs(req.text,"lxml")

select=False
j=1
for imagelistdiv in soup.findAll("div",{"class":"mw-category-group"}):
	if select == True:
		for li in imagelistdiv.findAll('li'):
			temp=li.find("a")
			link="https://en.wikipedia.org"+temp['href']
			data={}
			data['name']=temp['title']
			print(temp['title'])
			link.replace("","")
			img_link=getimgurl(link)
			data['wiki_link']=link
			if img_link is not None:
				img_data = requests.get(img_link).content
				file_name=str(j)
				if ".jpg" in img_link:
					file_name=file_name+'.jpg'
				elif ".png" in img_link:
					file_name=file_name+'.png'
				elif ".gif" in img_link:
					file_name=file_name+'.gif'
				else:
					file_name=file_name+'jpg'
				file_name="raw_data_winner/"+file_name
				with open(file_name, 'wb') as handler:
					handler.write(img_data)
				data['image_file']=file_name
			else:
				data['image_file']="not found"
			index.append(data)
			j=j+1
	select=True

tojson(filejson,index)
