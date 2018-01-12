import cv2
import os

def gray2rgb(filelist,savepath):
    for file in filelist:
        img = cv2.imread(file)
        try:
            newimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newimg = cv2.cvtColor(newimg,cv2.COLOR_GRAY2RGB)
        except:
            pass
        cv2.imwrite(savepath+'\\'+os.path.basename(file),newimg)