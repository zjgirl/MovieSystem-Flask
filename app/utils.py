import cv2
import numpy as np

#获取图像灰度值
def getGray(imgPath):
    img = cv2.imdecode(np.fromfile(imgPath, dtype=np.uint8), 0)
    height = img.shape[0]
    width = img.shape[1]
    gray = [0] * 256
    for h in range(height):
        for w in range(width):
            gray[img[h][w]] += 1
    gray = [str(i) for i in gray]
    return ','.join(gray)

#比较上传图像的灰度值和库里图片的灰度值
def compare(uplaodGray, sqlGray):
    imgUplaod = uplaodGray.split(',')
    imgSql = sqlGray.split(',')
    count = 0
    for i in range(0, 256):
        if int(imgUplaod[i]) == int(imgSql[i]):
            count += 1
    return count

#排序展示 sqlList是库里所有的电影
def sortPoster(uploadGray, sqlList):
    list = []
    for movie in sqlList:
        count = compare(uploadGray, movie.imageinfo)
        list.append([count, movie])
    #按照第一维从大到小排序
    list.sort(key=lambda x: x[0], reverse=True)
    #返回排好序的电影列表
    return [m for _, m in list]