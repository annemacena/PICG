import numpy as np
import matplotlib.pylab as plt
from PIL import Image

########################################
# funcoes auxiliares
def saturate(array_image):
    array_image[array_image > 255] = 255
    array_image[array_image < 0] = 0
    return array_image
def clamp(j, L):
    return min(max(j, 0), L-1)
########################################

# Q.2
def imread(path):
	return plt.imread(path)

# Q.3
def nchannels(array_image):
    return len(array_image.shape)

# Q.4
def size(array_image):
    shape = array_image.shape
    return [shape[1], shape[0]]

# Q.5
def rgb2gray(array_image):
    return np.dot(array_image[...,:3], [0.299, 0.587, 0.114]).astype('float')

# Q.6
def imreadgray(path):
    return rgb2gray(imread(path))

# Q.7
def imshow(array_image):
    if(nchannels(array_image) > 2):
        plt.imshow(array_image, interpolation='nearest')
    else: # grayscale
        plt.imshow(array_image, 'gray', interpolation='nearest')
    plt.show()

# Q.8
def thresh(array_image, t):
    return ((array_image >= t) * 255).astype(np.uint8)

# Q.9
def negative(array_image):
    return (255 - array_image).astype(np.uint8)

# Q.10
def contrast(img, r, m):
    result = r * (img - m) + m
    return saturate(result).astype(np.uint8)

# Q.11
def hist(array_image):
    column_m = []
    if nchannels(array_image) > 2: 
        column_m = [
            array_image[...][...][0].flatten(), # r
            array_image[...][...][1].flatten(), # g
            array_image[...][...][2].flatten()  # b
        ]
    else : # grayscale
        column_m = array_image.flatten()

    return column_m

# Q.12
def showhist(column_m):
    plt.hist(column_m)
    plt.show()

# Q.13
def showhist_bin(column_m, bin):
    plt.hist(column_m, bins=bin)
    plt.show()

# Q.14
def histeq(array_image):
    ni = hist(array_image)
    n = sum(ni)
    Pr = (ni/n) #probabilidade
    Tr = np.array([0] * 256)
    
    for k in range(1,255):
        Tr[k] = Pr[k] + Tr[k-1] #probabilidade acumulada

    return np.interp(array_image, range(0,256), Tr)

# Q.15
def convolve(array_image, mask):
    mask_w, mask_h = size(mask)
    mW = mask_w % 2
    mH = mask_h % 2
    image_width, image_height = size(array_image)
    convoluted = np.copy(array_image)

    if nchannels(array_image) > 2:
        for x in range(0,image_height):
            for y in range(0,image_width):
                t = 0
                for mx in range(-mH,mH):
                    for my in range(-mW,mW):                        
                        for c in range(3):
                            v = array_image[clamp(x+mx, image_height)][clamp(y+my, image_width)][c]
                            t = t + (mask[mx+mH][my+mW] * v)

                convoluted[x][y] = t
    else:
        for x in range(0,image_height):
            for y in range(0,image_width):
                t = 0
                for mx in range(-mH,mH):
                    for my in range(-mW,mW):
                        c = array_image[clamp(x+mx, image_height)][clamp(y+my, image_width)]
                        t = t + (mask[mx+mH][my+mW] * c)

                convoluted[x][y] = t

    return convoluted

# Q.16
def maskBlur():
    return np.array((0.0625) * np.array([[1,2,1],[2,4,2],[1,2,1]]))

# Q.17
def blur(array_image):
    return convolve(array_image, maskBlur())

# Q.18
def seSquare3():
    return np.array([[1,1,1],[1,1,1],[1,1,1]])

# Q.19
def seCross3():
    return np.array([[0,1,0],[1,1,1],[0,1,0]])

# Q.20
def erode(array_image, mask):
    mask_w, mask_h = size(mask)
    mW = mask_w % 2
    mH = mask_h % 2
    image_width, image_height = size(array_image)
    array_image2 = np.copy(array_image)

    for x in range(0,image_height):
            for y in range(0,image_width):
                t = np.array([], dtype=np.uint8)
                for mx in range(-mH,mH):
                    for my in range(-mW,mW):
                        t = np.append(array_image[clamp(x+mx, image_height)][clamp(y+my, image_width)], 3)

                array_image2[x][y] = np.amin(t)

    return array_image2

# Q.21
def dilate(array_image, mask):
    mask_w, mask_h = size(mask)
    mW = mask_w % 2
    mH = mask_h % 2
    image_width, image_height = size(array_image)
    array_image2 = np.copy(array_image)

    for x in range(0,image_height):
            for y in range(0,image_width):
                t = np.array([], dtype=np.uint8)
                for mx in range(-mH,mH):
                    for my in range(-mW,mW):
                        t = np.append(array_image[clamp(x+mx, image_height)][clamp(y+my, image_width)], 3)

                array_image2[x][y] = np.amax(t)

    return array_image2
