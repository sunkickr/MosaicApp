from PIL import Image
import glob
import math
import json
from datetime import datetime
import time
import random
from pathlib import Path
from sklearn.neighbors import NearestNeighbors
import numpy as np

def image_list(image, pixelnum):
    """makes list of small images from one image"""
    ratio = round(image.width/image.height, 1)
    size = (int(1000*ratio), int(1000))

    new = image.resize(size)
    col = int(size[0]/pixelnum)
    row = int(size[1]/pixelnum)
    image_list = []
    y1 = 0
    y2 = pixelnum
    x1 = 0
    x2 = pixelnum
    for i in range(row):
        for j in range(col):
            newim = new.crop((x1,y1,x2,y2))
            image_list.append(newim)
            x1 += pixelnum
            x2 += pixelnum
        x1 = 0
        x2 = pixelnum
        y1 += pixelnum
        y2 += pixelnum
    return image_list

def calcolor(image_list, pixelnum):
    div = pixelnum*pixelnum
    color_list = []
    for image in image_list:
        R =[]
        G = []
        B = []
        for i in range(pixelnum):
            for j in range(pixelnum):
                color = image.getpixel((i,j))
                R.append(color[0])
                G.append(color[1])
                B.append(color[2])
        avg_color = int(sum(R)/(div)), int(sum(G)/(div)), int(sum(B)/(div))
        color_list.append(avg_color)
    return color_list

def calsource2(path, pixelnum):
    """Calcualtes the average color of the source images."""
    div = pixelnum*pixelnum
    my_file = Path('mosaic_api/mosaicbuilder/color_dict.txt')
    if my_file.exists():

        with open('mosaic_api/mosaicbuilder/color_dict.txt') as json_file:
            color_dict = json.load(json_file)
        return color_dict
    else:
        color_dict = {}
        image_list = []
        color_list = []
        i = 0

        for i in range(1,2878):
            try:
                image =Image.open(path + "/img"+str(i)+".jpeg")
            except:
                print('error')
                continue
            R = []
            G = []
            B = []
            for i in range(pixelnum):
                for j in range(pixelnum):
                    color = image.getpixel((i,j))
                    try:
                        R.append(color[0])
                        G.append(color[1])
                        B.append(color[2])
                    except:

                        continue
            avg_color = sum(R)/(div), sum(G)/(div), sum(B)/(div)

            color_list.append(avg_color)
            filename = str(image.filename)
            image_list.append(filename)
            i+=1
        color_dict = {"color_list":color_list, "image_list":image_list}
        with open('mosaic_api/mosaicbuilder/color_dict.txt', 'w') as outfile:
            json.dump(color_dict, outfile)

        return color_dict

def match2(image_list, color_list, source_dict, path):
    source_list = source_dict["image_list"]
    source_color_list = source_dict["color_list"]
    mosaic_list = []
    print(len(image_list))
    print(len(color_list))
    print(len(source_list))
    print(len(source_color_list))
    colorgraph4 = NearestNeighbors(radius=10).fit(source_color_list)
    colorgraph7 = NearestNeighbors(radius=26).fit(source_color_list)
    image_color = tuple(zip(image_list, color_list))
    for image, color in image_color:
        try:
            rng4 = colorgraph4.radius_neighbors([color])
            array4 = np.asarray(rng4[1][0])
            choice = source_list[random.choice(array4)]

        except:
            try:
                rng7 = colorgraph7.radius_neighbors([color])
                array7 = np.asarray(rng7[1][0])
                choice = source_list[random.choice(array7)]

            except:
                dislist =[]
                i = 0
                for sc in source_color_list:
                    dis = math.sqrt( (sc[0]-color[0])**2 + (sc[1] - color[1])**2
                        + (sc[2] - color[2])**2)
                    dislist.append(dis)
                    if dis == min(dislist):
                        ans = dis
                        choice = source_list[i]
                    i += 1
                print(ans)

        tup = (image, choice)
        mosaic_list.append(tup)

    return mosaic_list

def build(mosaic_list, image, pixelnum, pixelnum2):
    ratio = round(image.width/image.height, 1)
    size = (int(1000*ratio), int(1000))
    col = int(size[0]/pixelnum)
    row = int(size[1]/pixelnum)
    size = (pixelnum2*col, pixelnum2*row)
    mosaic = Image.new('RGB', size)
    num = -1
    y1, x1 = 0, 0
    x2, y2 = pixelnum2, pixelnum2
    for i in range(row):
        for j in range(col):
            num+=1

            mosaic.paste(Image.open(mosaic_list[num][1]), (x1,y1,x2,y2))
            x1+=pixelnum2
            x2+=pixelnum2
        x1 = 0
        x2 = pixelnum2
        y1+= pixelnum2
        y2+= pixelnum2

    return mosaic



def create_mosaic(image, pixelnum, pixelnum2, path):

    
    image_li = image_list(image, pixelnum)
    color_list = calcolor(image_li, pixelnum)

    source_dict = calsource2(path, pixelnum2)

    mosaic_list = match2(image_li, color_list, source_dict, path)
    
    mosaic = build(mosaic_list, image, pixelnum, pixelnum2)
    
    return mosaic






