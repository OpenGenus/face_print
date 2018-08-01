import cv2
import sys
import os

class FaceCropper(object):
    #CASCADE_PATH to be replaced with corresponding path containing "haarcascade_frontalface_default.xml"

    CASCADE_PATH = "/home/tanmay/opencv/data/haarcascades/haarcascade_frontalface_default.xml"

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(self.CASCADE_PATH)

    def generate(self, image_path,new_path,i):
        imageloc=""
        folder=""

        img = cv2.imread(image_path)
        if (img is None):
            print("Can't open image file")
            imageloc="not found"
            folder="no"
            return imageloc,folder

        faces = self.face_cascade.detectMultiScale(img, 1.3, 5, minSize=(20, 20))
        if (faces is None):
            print('Failed to detect face')
            imageloc="not found"
            folder="no"
            return imageloc,folder

        facecnt = len(faces)
        print("Detected faces: %d" % facecnt)
        height, width = img.shape[:2]
        if facecnt>1:
            new_folder=new_path+'/'+str(i)
            imageloc='raw_data_winner_cropped/'+str(i)
            folder='yes'
            os.makedirs(new_folder)
            j=1
            for (x, y, w, h) in faces:
                r = max(w, h) / 2
                centerx = x + w / 2
                centery = y + h / 2
                nx = int(centerx - r)
                ny = int(centery - r)
                nr = int(r * 2)

                faceimg = img[ny:ny+nr, nx:nx+nr]
                lastimg = cv2.resize(faceimg, (200, 200))
                cv2.imwrite('''raw_data_winner_cropped/{0}/image{1}.jpg'''  .format(i,j), lastimg)
                j=j+1
            return imageloc,folder
        elif facecnt==1:
            folder='no'
            for (x, y, w, h) in faces:
                r = max(w, h) / 2
                centerx = x + w / 2
                centery = y + h / 2
                nx = int(centerx - r)
                ny = int(centery - r)
                nr = int(r * 2)

                faceimg = img[ny:ny+nr, nx:nx+nr]
                lastimg = cv2.resize(faceimg, (200, 200))
                cv2.imwrite("raw_data_winner_cropped/image{0}.jpg" .format(i), lastimg)
                imageloc="raw_data_winner_cropped/image{0}.jpg" .format(i)
                return imageloc,folder
        elif facecnt==0:
            return "not found","no"

detecter = FaceCropper()