from scan_files import scan_files
from gray2rgb import gray2rgb
filelist = scan_files('E:\\mountain_decolor')
gray2rgb(filelist,'E:\\mountain_decolor2rgb')
#
# img = cv2.imread('E:\\inkdecolor\\decolor_he1.jpg')
# newimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# newimg = cv2.cvtColor(newimg,cv2.COLOR_GRAY2RGB)
# cv2.imshow('test',newimg)
# cv2.waitKey(0)
#filelist = scan_files('E:\\decolor2rgb\\liu')

#gray2rgb(filelist,'E:\\decolor2rgb')
# print(predict('E:\\ink\\bird1.jpg'))
