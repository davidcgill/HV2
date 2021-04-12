import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np
import cv2
import http.client as client
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
import io


flag=0

cap = cv2.VideoCapture(0)
def getRectangle(faceDictionary):
                    rect = faceDictionary['faceRectangle']
                    left = rect['left']
                    top = rect['top']
                    bottom = left + rect['height']
                    right = top + rect['width']
                    return ((left, top), (bottom, right))
                
def read_data(name):

    f = open("HackTheValley2.txt", "r")
    a=[]
    i = 0
    for line in f:
        word = line.split('\n')
        a.append(word[0])
        i += 1
    f.close()


    mass = [[]for k in range (5)]    
    for i in range (5):
       for j in range (i*4, i*4+4):
           mass[i].append(a[j])
           

    while j in range(1, 3):
        int(a[j])


    if name == mass[i][0]:
        print("Credit Card Number:" + mass[i][1])
        print("Expiration Date:" + mass[i][2])
        print("Security Code:" + mass[i][3])
    else:
        i += 1


def matchcheck():
        

        customers=1

        for filenum in range (customers):
            infile= open("myface{}.txt".format(filenum))
            for i in range (5):
                img_url1 = infile.readline()
        #faces = CF.face.detect(img_url)
        infile.close()
        #print(img_url1)
        face1=extractid(img_url1)
        #this one comes from the jpg
        #filename='C:\\Users\\david\\Desktop\\htv2\\pic.jpg'
        #url2 = io.open(filename,'rb')


        face2=extractid('https://davidcgill.blob.core.windows.net/mycontainer/pic.jpg')
        #url2.close()
        sub_KEY = '70f27271f2f2484fa11d07678763266b'  # Replace with a valid Subscription Key here.
        CF.Key.set(sub_KEY)
        
        headers = { 'Ocp-Apim-Subscription-Key': sub_KEY
                }
       

        BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/verify/'  # Replace with your regional Base URL
        CF.BaseUrl.set(BASE_URL)  # switch this to a verify / compare
        
        response = requests.post(BASE_URL, headers=headers, json={"faceId1": face1, "faceId2": face2})
        faces = response.json()
        #HTML("<font size=5>Detected <font color='blue'>%d</font> faces in the image</font>"%len(faces))
      
        print (faces)
        checkstr="{}".format(faces)
        wordlist1=[]
        for i in range (3):
                wordlist1.append(checkstr[i+36])
        checkstr=''.join(wordlist1)
        print(float(checkstr))
        if float(checkstr)>= 0.8:
                print("yay")
                return 1
        print("boo")
   
        return 0



def get_image():
    # Captures a single image from the camera and returns it in PIL format
        reval,im= cap.read()
        return im
def extractid(img_url):
    sub_KEY = '70f27271f2f2484fa11d07678763266b'  # Replace with a valid Subscription Key here.
    CF.Key.set(sub_KEY)

    BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/detect/'  # Replace with your regional Base URL
    CF.BaseUrl.set(BASE_URL)

    #img_url = 'http://images.glaciermedia.ca/polopoly_fs/1.22388631.1504445194!/fileImage/httpImage/image.jpg_gen/derivatives/landscape_804/a4-2082-jpg.jpg'
    #faces = CF.face.detect(img_url)

    headers = { 'Ocp-Apim-Subscription-Key': sub_KEY }

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,smile',
    }

    response = requests.post(BASE_URL, params=params, headers=headers, json={"url": img_url})
    faces = response.json()
    #HTML("<font size=5>Detected <font color='blue'>%d</font> faces in the image</font>"%len(faces))
    print (img_url)
    print (faces)
    writestr="{}".format(faces)
    wordlist=[]
    for i in range (36):
        wordlist.append(writestr[i+13])
    writestr=''.join(wordlist)
    print(writestr)
    return writestr

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    
    
    if (flag):
        flag=matchcheck()
        if (flag):
                break
        else:
                flag=0
        #analysize photo in this loop and then break if  it is clear to go and compare agaist the world

    ramp_frames = 5
    if cv2.waitKey(1) & 0xFF == ord('y'):
         for i in range(ramp_frames):
            temp = get_image()
         print ("Taking image..")
         camera_capture=get_image()
         file = "pic.jpg"
         cv2.imwrite(file, camera_capture)
         block_blob_service = BlockBlobService(account_name='davidcgill', account_key='ybj8fnpScqtmFbbRFNwhd5U3pSrs+tr35Po2zdb4qYSMcyvB7sBHxyO0moZRuYB4t12K1K6ZRTPW+GAE8yKU9g==')
         block_blob_service.create_blob_from_path(
                    'mycontainer',
                    'pic.jpg',
                    'C:\\Users\\david\\Desktop\\htv2\\pic.jpg',
                    content_settings=ContentSettings(content_type='image/jpg')
                            )
         while (1):
                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                 if cv2.waitKey(1) & 0xFF == ord('y'):
                        flag=1
                        break
                 elif cv2.waitKey(1) & 0xFF == ord('n'):
                        flag=0
                        break
         
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()





