# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 03:57:42 2020

@author: narendran.n
"""

import cv2
import os
import pyzbar.pyzbar as pyzbar


os.chdir(r"C:\Users\Public\Documents\hackathon")
img=cv2.imread("qrcode_6.jpeg")
cv2.imshow("Image", img)

decodeobjects=pyzbar.decode(img)



for obj in decodeobjects:
    obj_d = obj.data.decode('utf-8')
obj_d = obj_d.strip("][").split("], [")
new_obj=[]
for objs in obj_d:
    new_obj.append(objs.split(", "))


new_obj2=[]
k=[]
for objcts in new_obj:
    v=str(objcts).replace("\'","_").replace("\"","").replace("_", "\\\"").replace("]","").replace("[","").replace(", ",":")
    v=v.upper()
    k.append(v)
k=", ".join(k)
k="\"{"+k+"}\""



import requests
url = "https://hackathon-cloud-291419.wl.r.appspot.com/details_products"
payload = "{\"HEINZ\":\"1\", \"ZOBO\":\"1\", \"ECHO DOT\":\"1\", \"ANNIE\":\"2\", \"DASAN\":\"2\"}"
headers = {
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data = payload)
print(response.text.encode('utf8'))
