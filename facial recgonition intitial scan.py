import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw


sub_KEY = '70f27271f2f2484fa11d07678763266b'  # Replace with a valid Subscription Key here.
CF.Key.set(sub_KEY)

BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/detect/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

img_url = 'https://davidcgill.blob.core.windows.net/mycontainer/headshotsuit.jpg'
#faces = CF.face.detect(img_url)

headers = { 'Ocp-Apim-Subscription-Key': sub_KEY }

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'gender',
}

response = requests.post(BASE_URL, params=params, headers=headers, json={"url": img_url})
faces = response.json()
#HTML("<font size=5>Detected <font color='blue'>%d</font> faces in the image</font>"%len(faces))

print (faces)
outfile = open ("myface0.txt","w")
creditinfo=[]
name= (input("Please input your Full name"))
creditinfo.append(input("Credit Card number"))
creditinfo.append(input("credit card expirery date"))
creditinfo.append(input("ccv code on the back"))
writestr= "Name:"+name+"\nCredit card number: "+creditinfo[0]+"\nCredit card expirery: "+creditinfo[1]+"\nCredit card ccv: "+creditinfo[2]
print(writestr, file=outfile)
print (img_url,file=outfile)
print(faces, file=outfile)
outfile.close()

#Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

#Download the image from the url
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))

#For each face returned use the face rectangle and draw a red box.
draw = ImageDraw.Draw(img)
for face in faces:
    draw.rectangle(getRectangle(face), outline='red')
#Display the image in the users default image browser.
img.show()
