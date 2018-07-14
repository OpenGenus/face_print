from bs4 import BeautifulSoup as bs
import requests
import lxml
import os
import json

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

filejson='image_mapping.json'
index=[]

url="https://en.wikipedia.org/wiki/List_of_computer_scientists"
req=requests.get(url)
soup=bs(req.text,"lxml")
text="""<div id="custom_div_images_opengenus">"""
toaddintag=soup.find("span",{"id":"A"})
tag=soup.find("span",{"id":"See_also"})
toaddintag.insert_after(text)
text="</div>"
tag.insert_before(text)

with open('out.html','w') as f:
	f.write(str(soup.prettify(formatter=None)))
soup = bs(open("out.html"), "lxml")

imagelistdiv=soup.find("div",{"id":"custom_div_images_opengenus"})
i=1
for li in imagelistdiv.findAll('li'):
	temp=li.find("a")
	link="https://en.wikipedia.org"+temp['href']
	link.replace(" ","")
	temp=temp.text
	temp.replace(" ","")
	print(temp)
	data={}
	data['name']=temp
	data['wiki_link']=link
	img_link=getimgurl(link)
	if img_link is not None:
	    img_data = requests.get(img_link).content
	    file_name=str(i)
	    if ".jpg" in img_link:
	    	file_name=file_name+'.jpg'
	    elif ".png" in img_link:
	        file_name=file_name+'.png'
	    elif ".gif" in img_link:
	        file_name=file_name+'.gif'
	    else:
	    	file_name=file_name+'jpg'
	    with open(file_name, 'wb') as handler:
		    handler.write(img_data)
	    data['image_file']=file_name
	else:
		data['image_file']="not found"
	index.append(data)
	i=i+1
	if i==51:
		break

tojson(filejson,index)
os.remove("out.html")
