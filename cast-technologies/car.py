
import cv2
import pandas as pd
import os 

df = pd.DataFrame(columns=['frameNo', 'topLeft', 'bottomRight'])

#given information: the first car location
img = cv2.imread('tracking-data/00001.jpg',0)
car=img[330:455, 420:610]

#given initial position of the car
cv2.imwrite('car.jpg',car)

#scaling factor in # of pixels
scale=2 
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

#GIVEN: size_change AND occlusion
occlusion=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
size_change=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1]

count=0

img_array = []
size = (0,0)

for i, nextFrame in enumerate(os.listdir('tracking-data')):

    img = cv2.imread('tracking-data/'+nextFrame,0)
    
    #check for occlusion, if occlusion true, do not update template
    if occlusion[i-1] == 0:
        template=car
        
    #check if size change, if yes, rescale template
    #before matching
    if size_change[i-1]==1:
        count=count+1

    #if two frames changed size, resize template
    if (size_change[i-1]==1 and count == 2):
        template = cv2.resize(template,(scale+w, scale+h), interpolation = cv2.INTER_LINEAR)
        count=0
    w, h = template.shape[::-1]

    #template/patch matching
    for meth in methods:
        #use matchTemplate
        method = eval(meth)
        res = cv2.matchTemplate(img,template,method)
        
        #get min,max
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        #get top left coordinate
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
            
        #get bottom right coordinate
        bottom_right = (top_left[0] + w, top_left[1] + h)
 
        #set new template
        car=img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        image = cv2.rectangle(img, top_left, bottom_right, (0,255,0),3)


        cv2.imwrite('car_output/car'+str(i)+'.jpg',image)

        height, width = image.shape
        size = (width,height)
        img_array.append(image)


        df = df.append(pd.DataFrame(data=[[i, top_left, bottom_right,]], columns=['frameNo', 'topLeft', 'bottomRight']))
        
    df.to_csv('car_position.csv')

print(img_array)
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()