import face_cropper_rawdata
import json
import os

def tojson(fileopen,data):
	with open(fileopen,'w') as f1:
		f1.write("{\"index\":")
		json.dump(data,f1,indent=2)
		f1.write("}")

with open('raw_data/image_mapping.json') as f:
    jsn = json.load(f)

datas=jsn["index"]

new_path = os.path.dirname(os.path.realpath(__file__))
new_path=new_path+'/raw_data_cropped'
os.makedirs(new_path)

i=1
index=[]
imageloc=""
folder=""

filejson="raw_data_cropped/cropped_image_mapping.json"

for data in datas:
	dat={}
	dat['name']=data["name"]
	path=data["image_file"]
	if(path != 'not found'):
		print(path)
		imageloc,folder=face_cropper_rawdata.detecter.generate(path,new_path,i)
		dat['image_file']=imageloc
		dat['folder']=folder
	else:
		dat['image_file']="not found"
		dat['folder']="no"
	index.append(dat)
	i=i+1

tojson(filejson,index)
