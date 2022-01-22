from cv2 import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class TextRead:
    def __init__(self,imPath, learnedChar, modelPath):
        self.text = ""
        self.im = cv2.imread(imPath)
        self.height, self.width, _ = self.im.shape
        self.learnedChar = learnedChar
        self.sizeShape=(64,64)
        if modelPath==None:
            self.text="Set Model Path!"
        else:
            self.model = load_model(modelPath)
            self.extractChar()

    def __str__(self):
        """
        This method is called when print() or str() function is invoked on an object.
        """
        return self.text

    def extractChar(self):
        """
        This method prepares an image and extracts individual objects,
        for each object it calls a method that reads this object.
        """
        #color change to shades of gray
        gray = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 50, 150, cv2.THRESH_BINARY)
        blurred = cv2.GaussianBlur(thresh, (3, 3), 0)
        binary = cv2.Canny(blurred, 50, 150)
        kernel = np.ones((3,3),np.uint8)
        dilate = cv2.dilate(binary, kernel, iterations=1)
        #extract objects
        cnts, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        (cnts, _) = self.sort_contours(cnts)
        #for each object we outline the object on original image and extract char
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(self.im, (x, y), (x + w, y + h), (0,0,255), 2)
            self.extractSingleCharFromImg(x,y,w,h,gray)

    def extractSingleCharFromImg(self, x, y, w, h):
        """
        This method returns extract single char from image.
        """
        obj=self.im[y:y+h,x:x+w]
        _,obj = cv2.threshold(obj,100,255,cv2.THRESH_BINARY)
        #set the borders (extra padding to your image)
        obj= cv2.copyMakeBorder(obj,10,10,10,10,cv2.BORDER_CONSTANT,value=(255,255,255))
        obj = cv2.medianBlur(obj.copy(),3)
        obj = cv2.resize(obj.copy(),self.sizeShape,interpolation = cv2.INTER_AREA)
        obj=(image.img_to_array(obj))/255
        obj=np.expand_dims(obj, axis = 0)
        result = self.model.predict(obj)
        np.reshape(result, len(self.learnedChar))
        high = np.amax(obj)
        low = np.amin(obj)
        if high != low:
            maxval = np.amax(result)
            index = np.where(result == maxval)
            self.text += self.learnedChar[index[1][0]]

    def getImg(self):
        """
        This method returns image.
        """
        return self.convert_cv_qt(self.im)

    def convert_cv_qt(self, cv_img):
        """
        Convert from an opencv image to QPixmap.
        """
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.width, self.height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def sort_contours(self,cnts):
        """
        Aligns the objects in the correct order from left to right.
        """
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),key=lambda b:b[1][0], reverse=False))
        return (cnts, boundingBoxes)