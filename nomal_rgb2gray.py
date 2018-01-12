import scan_files
import cv2
import os

def nomal_rgb2gray(filelist,savepath):
    for file in filelist:
        img = cv2.imread(file)
        try:
            newimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            pass
        cv2.imwrite(savepath+'\\'+os.path.basename(file),newimg)