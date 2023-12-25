import cv2
from pyzbar.pyzbar import decode
import requests
import numpy as np
import imutils

def formatURL(url):
    return url + "/shot.jpg"

urls = ["http://192.168.5.157:8080" ,]
address = []
for url in urls:
    address.append(formatURL(url))

while True:
    img_resps = []
    for url in urls:
        img_resps.append(requests.get(url))
    img_arrs = []
    for resp in img_resps:
        img_arrs.append(np.array(bytearray(resp.content), dtype=np.uint8))
    imgs = []
    for arr in img_arrs:
        imgs.append(cv2.imdecode(arr, -1))
    img_formated = []
    for index, img in enumerate(imgs):
        cv2.imshow("Camera: " + str(index), imutils.resize(img, width=1000, height=1800))
    
    if cv2.waitKey(1) == 27:
        break
        
    # img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    # img = cv2.imdecode(img_arr, -1)
    # img = imutils.resize(img, width=1000, height=1800)
    # cv2.imshow("Android_cam", img)

    # if cv2.waitKey(1) == 27:
    #     break

cv2.destroyAllWindows()



# screen = cv2.VideoCapture(0)
# screen.set(3, 640)
# screen.set(4,480)
# isCapture = True
# while isCapture == True:
#     success, frame = screen.read()
#     isDecodeFrameComplete = False
#     decodeFrame = None
#     while not isDecodeFrameComplete:
#         try:
#             decodeFrame = decode(frame)
#             isDecodeFrameComplete = True
#         except:
#             continue
#     cv2.imshow('Testing-code-scan', frame)
#     if cv2.waitKey(1) == 27:
#         break