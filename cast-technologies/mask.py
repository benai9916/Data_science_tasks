import numpy as np
import cv2, os
import cv2 as cv

for no,img in enumerate(os.listdir('data/')):
    img = cv.imread('data/'+img)
    # img = cv2.imread('data/1081face0.jpg')
    Z = np.float32(img.reshape((-1,3)))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 4
    _,labels,centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    labels = labels.reshape((img.shape[:-1]))
    reduced = np.uint8(centers)[labels]

    result = [np.hstack([img, reduced])]
    for i, c in enumerate(centers):
        mask = cv2.inRange(labels, i, i)
        mask = np.dstack([mask]*3) # Make it 3 channel
        ex_img = cv2.bitwise_and(img, mask)
        ex_reduced = cv2.bitwise_and(reduced, mask)
        result.append(np.hstack([ex_img, ex_reduced]))

        cv2.imwrite('out2/'+str(no)+'.jpg', np.vstack(result))


