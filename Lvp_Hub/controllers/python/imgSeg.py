import sys
import random
import string
import os
def makeFolder():
    
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    path = "./controllers/python/output/"+result_str+"/"
    os.mkdir(path)
    return path

def imgSeg(imgCount, img_urls):

        #savePath = makeFolder()
        #print(savePath)
        count = 0
        path = img_urls.split(',')
        
        imgCount = int(imgCount)
        
        while "/" in path:
            path.remove('/')
            imgCount = imgCount -1

        for i in range(imgCount)):
            from urllib import request
            import cv2
            import numpy as np

            # URL to image
            resp = request.urlopen(path[i])
            img = np.asarray(bytearray(resp.read()), dtype="uint8")
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray, cv2.CV_8UC1)
            sobel = cv2.Sobel(gray, cv2.CV_8UC1, 0, 1, ksize= 3)

            # Remove some small noise if any.
            dilate = cv2.dilate(sobel,None)
            erode = cv2.erode(dilate,None)

            ret,thresh1 = cv2.threshold(erode,127,255,cv2.THRESH_BINARY)

            # Find contours with cv2.RETR_CCOMP
            contours, hierarchy = cv2.findContours(erode, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]

            # Get width, height of origin image
            height, width, channels = img.shape
            # Temp criteria of width
            tempWidth = width - 100

            tempY = height
            
            for i,cnt in enumerate(contours):
                # Check if it is an external contour and its area is more than 100
                if hierarchy[0,i,3] == -1 : 
                    x,y,w,h = cv2.boundingRect(cnt)
                    if(w > tempWidth):
                            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

                            m = cv2.moments(cnt)
                            tempHeight = height -( height- tempY )

                            if( tempHeight -y > 100 ) :
                                count += 1
                                cv2.imwrite(savePath+"Img"+str(count)+".jpg", img[y:tempHeight, 0:0+width])
                                tempY = y
            if(tempY > 10):
                    count += 1
                    cv2.imwrite(savePath+"Img"+str(count)+".jpg", img[0:tempY, 0:0+width])
            print(count)        
            #cv2.imwrite("output/Img"+str(count)+".jpg", img[0:tempY, 0:0+width])
            #cv2.imshow('img', temp)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()


imgSeg(sys.argv[1], sys.argv[2])
