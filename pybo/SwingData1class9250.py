# -*- coding: utf-8 -*-
"""
15:44
SwingData1 class 정의하는 파일
mpu9250만 연결된 상태, 7가지 값을 받음
"""

# 업로드할 때마다 바꿔줘야 함
#url = 'http://192.168.219.115/'
#pathBase = "C:/Users/hp/Desktop/bowlingData0609/"


from .SwingAttributeClass9250 import SwingAttribute

# 매번 바꿔줘야 함
#pathBase = "C:/Users/hp/Desktop/bowlingData0609/"  # 하위폴더로 c, ss, so가 있고 그 안에 txt 형태 데이터들이 들어있음


import requests
import numpy as np
import matplotlib.pyplot as plt
# title 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
"""
#font_path = "C:/Windows/Fonts/NGULIM.TTF"
font_path = "C:/Users/hp/AppData/Local/Microsoft/Windows/Fonts/NotoSansCJKkr-Regular.otf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
"""

import datetime

def Load_Data(path):
    f = open(path)
    txt = f.readlines()
    loaded_data = []
    for i in range(len(txt)):
        row = txt[i].split("\t")
        row.pop()
        row = list(map(float, row))
        loaded_data.append(row)
    f.close()
    return loaded_data


class SwingData1:

    def __init__(self, filename, data, pathBase):

        """

        *input*

        filename: django에서 입력한 이름 + ".txt"

        data: url에서 request -> array(7*501)

        pathBase: 저장할 최하위 폴더 path

        """

        #self.Type = Type
        self.filename = filename
        self.pB = pathBase
        self.path = "./static/pybo/objects/" + filename
        self.data = data

        #손목 mpu9250
        self.t1 = self.data[0]
        self.gx1 = self.data[1]
        self.gy1 = self.data[2]
        #그래프 매끈하게 만들기
        self.gy1 = self.smooth(self.gy1, 6)

        self.gz1 = self.data[3]
        self.ax1 = self.data[4]
        self.ay1 = self.data[5]
        self.az1 = self.data[6]

        '''
        #팔꿈치 mpu6050
        self.t2 = self.data[7]
        self.gx2 = self.data[8]
        self.gy2 = self.data[9]
        self.gz2 = self.data[10]
        self.ax2 = self.data[11]
        self.ay2 = self.data[12]
        self.az2 = self.data[13]
        '''

        self.attr = SwingAttribute(self)

        """
        #시작시간 0으로 맞춤
        self.t1 = [self.t1[i] - self.t1[0] for i in range(len(self.t1))]
        self.t2 = [self.t2[i] - self.t1[0] for i in range(len(self.t2))]
        """

    def smooth(self, dataArr, n):
        arrLen = len(dataArr)
        smoothArr = []
        for i in range(n):
            dataArr.append(dataArr[arrLen - 1])

        for i in range(arrLen):
            smoothVal = dataArr[i]
            for j in range(n):
                smoothVal += dataArr[i + j]
            smoothVal /= n
            smoothArr.append(smoothVal)

        return smoothArr


    def save(self):
        f = open(self.path, 'w')
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                f.write(str(self.data[i][j]))
                f.write('\t')
            f.write('\n')
        f.close()

    def plot(self):

        plt.subplot(121)
        plt.plot(self.t1, self.gx1, label = "x")
        plt.plot(self.t1, self.gy1, label = "y")
        plt.plot(self.t1, self.gz1, label = "z")
        #plt.plot([self.attr.pushAway.t1, self.attr.pushAway.t1, self.attr.pushAway.t1], [self.attr.pushAway.gx1, self.attr.pushAway.gy1,self.attr.pushAway.gz1], '.', label = "pushAway")
        plt.plot([self.attr.downSwing1.t1, self.attr.downSwing1.t1, self.attr.downSwing1.t1], [self.attr.downSwing1.gx1, self.attr.downSwing1.gy1, self.attr.downSwing1.gz1], 'x', label = "downSwing")

        """
        elbowCheckEnd plotting
        """
        #plt.plot(self.t1[self.attr.downSwing1.index + 53], self.gy1[self.attr.downSwing1.index + 53], 's', label = "elbowCheckEnd")



        #plt.plot([self.attr.downSwing2.t1, self.attr.downSwing2.t1, self.attr.downSwing2.t1], [self.attr.downSwing2.gx1, self.attr.downSwing2.gy1, self.attr.downSwing2.gz1], '.', label = "downSwing2")
        plt.plot([self.attr.backSwingBtm.t1, self.attr.backSwingBtm.t1, self.attr.backSwingBtm.t1], [self.attr.backSwingBtm.gx1, self.attr.backSwingBtm.gy1, self.attr.backSwingBtm.gz1], 'x', label = "backSwingBtm")
        plt.plot([self.attr.backSwingTop.t1, self.attr.backSwingTop.t1, self.attr.backSwingTop.t1], [self.attr.backSwingTop.gx1, self.attr.backSwingTop.gy1, self.attr.backSwingTop.gz1], 'x', label = "backSwingTop")
        plt.plot([self.attr.fwdSwingBtm.t1, self.attr.fwdSwingBtm.t1, self.attr.fwdSwingBtm.t1], [self.attr.fwdSwingBtm.gx1, self.attr.fwdSwingBtm.gy1, self.attr.fwdSwingBtm.gz1], 'x', label = "fwdSwingBtm")
        plt.plot([self.attr.release.t1, self.attr.release.t1, self.attr.release.t1], [self.attr.release.gx1, self.attr.release.gy1, self.attr.release.gz1], 'o', label = "release")
        plt.plot([self.attr.flThrTop.t1, self.attr.flThrTop.t1, self.attr.flThrTop.t1], [self.attr.flThrTop.gx1, self.attr.flThrTop.gy1, self.attr.flThrTop.gz1], 'x', label = "flThrTop")
        #plt.legend(loc='upper right', bbox_to_anchor=(1,1))
        plt.xlabel("time[ms]")
        plt.ylabel("gyro by mpu9250[deg/s] (wrist)")

        plt.subplot(122)
        plt.plot(self.t1, self.ax1, label = "x")
        plt.plot(self.t1, self.ay1, label = "y")
        plt.plot(self.t1, self.az1, label = "z")
        #plt.plot([self.attr.pushAway.t1, self.attr.pushAway.t1, self.attr.pushAway.t1], [self.attr.pushAway.ax1, self.attr.pushAway.ay1,self.attr.pushAway.az1], '.', label = "pushAway")
        plt.plot([self.attr.downSwing1.t1, self.attr.downSwing1.t1, self.attr.downSwing1.t1], [self.attr.downSwing1.ax1, self.attr.downSwing1.ay1, self.attr.downSwing1.az1], 'x', label = "downSwing")
        plt.plot([self.attr.backSwingBtm.t1, self.attr.backSwingBtm.t1, self.attr.backSwingBtm.t1], [self.attr.backSwingBtm.ax1, self.attr.backSwingBtm.ay1, self.attr.backSwingBtm.az1], 'x', label = "backSwingBtm")
        plt.plot([self.attr.backSwingTop.t1, self.attr.backSwingTop.t1, self.attr.backSwingTop.t1], [self.attr.backSwingTop.ax1, self.attr.backSwingTop.ay1, self.attr.backSwingTop.az1], 'x', label = "backSwingTop")
        plt.plot([self.attr.fwdSwingBtm.t1, self.attr.fwdSwingBtm.t1, self.attr.fwdSwingBtm.t1], [self.attr.fwdSwingBtm.ax1, self.attr.fwdSwingBtm.ay1, self.attr.fwdSwingBtm.az1], 'x', label = "fwdSwingBtm")
        plt.plot([self.attr.release.t1, self.attr.release.t1, self.attr.release.t1], [self.attr.release.ax1, self.attr.release.ay1, self.attr.release.az1], 'o', label = "release")
        plt.plot([self.attr.flThrTop.t1, self.attr.flThrTop.t1, self.attr.flThrTop.t1], [self.attr.flThrTop.ax1, self.attr.flThrTop.ay1, self.attr.flThrTop.az1], 'x', label = "flThrTop")
        plt.legend(loc = 'upper left', bbox_to_anchor=(1,1))
        plt.xlabel("time[ms]")
        plt.ylabel("acc by mpu9250[g] (wrist)")

        '''
        plt.subplot(233)
        plt.plot(self.t1, self.mx, label = "x")
        plt.plot(self.t1, self.my, label = "y")
        plt.plot(self.t1, self.mz, label = "z")
        plt.plot([self.attr.pushAway.t1, self.attr.pushAway.t1, self.attr.pushAway.t1], [self.attr.pushAway.mx, self.attr.pushAway.gy1,self.attr.pushAway.mz], '.', label = "pushAway")
        plt.plot([self.attr.downSwing1.t1, self.attr.downSwing1.t1, self.attr.downSwing1.t1], [self.attr.downSwing1.mx, self.attr.downSwing1.my, self.attr.downSwing1.mz], '.', label = "downSwing")
        plt.plot([self.attr.backSwingBtm.t1, self.attr.backSwingBtm.t1, self.attr.backSwingBtm.t1], [self.attr.backSwingBtm.mx, self.attr.backSwingBtm.my, self.attr.backSwingBtm.mz], '.', label = "backSwingBtm")
        plt.plot([self.attr.backSwingTop.t1, self.attr.backSwingTop.t1, self.attr.backSwingTop.t1], [self.attr.backSwingTop.mx, self.attr.backSwingTop.my, self.attr.backSwingTop.mz], '.', label = "backSwingTop")
        plt.plot([self.attr.fwdSwingBtm.t1, self.attr.fwdSwingBtm.t1, self.attr.fwdSwingBtm.t1], [self.attr.fwdSwingBtm.mx, self.attr.fwdSwingBtm.my, self.attr.fwdSwingBtm.mz], '.', label = "fwdSwingBtm")
        plt.plot([self.attr.release.t1, self.attr.release.t1, self.attr.release.t1], [self.attr.release.mx, self.attr.release.my, self.attr.release.mz], '.', label = "release")
        plt.plot([self.attr.flThrTop.t1, self.attr.flThrTop.t1, self.attr.flThrTop.t1], [self.attr.flThrTop.mx, self.attr.flThrTop.my, self.attr.flThrTop.mz], '.', label = "flThrTop")
        plt.legend(loc='upper right', bbox_to_anchor=(1,0))
        plt.xlabel("time[ms]")
        plt.ylabel("mag by mpu9250[?] (wrist)")

        plt.subplot(223)
        plt.plot(self.t2, self.gx2, label = "x")
        plt.plot(self.t2, self.gy2, label = "y")
        plt.plot(self.t2, self.gz2, label = "z")
        plt.plot([self.attr.pushAway.t2, self.attr.pushAway.t2, self.attr.pushAway.t2], [self.attr.pushAway.gx2, self.attr.pushAway.gy2,self.attr.pushAway.gz2], '.', label = "pushAway")
        plt.plot([self.attr.downSwing1.t2, self.attr.downSwing1.t2, self.attr.downSwing1.t2], [self.attr.downSwing1.gx2, self.attr.downSwing1.gy2, self.attr.downSwing1.gz2], '.', label = "downSwing")
        plt.plot([self.attr.downSwing2.t2, self.attr.downSwing2.t2, self.attr.downSwing2.t2], [self.attr.downSwing2.gx2, self.attr.downSwing2.gy2, self.attr.downSwing2.gz2], '.', label = "downSwing2")
        plt.plot([self.attr.backSwingBtm.t2, self.attr.backSwingBtm.t2, self.attr.backSwingBtm.t2], [self.attr.backSwingBtm.gx2, self.attr.backSwingBtm.gy2, self.attr.backSwingBtm.gz2], '.', label = "backSwingBtm")
        plt.plot([self.attr.backSwingTop.t2, self.attr.backSwingTop.t2, self.attr.backSwingTop.t2], [self.attr.backSwingTop.gx2, self.attr.backSwingTop.gy2, self.attr.backSwingTop.gz2], '.', label = "backSwingTop")
        plt.plot([self.attr.fwdSwingBtm.t2, self.attr.fwdSwingBtm.t2, self.attr.fwdSwingBtm.t2], [self.attr.fwdSwingBtm.gx2, self.attr.fwdSwingBtm.gy2, self.attr.fwdSwingBtm.gz2], '.', label = "fwdSwingBtm")
        plt.plot([self.attr.release.t2, self.attr.release.t2, self.attr.release.t2], [self.attr.release.gx2, self.attr.release.gy2, self.attr.release.gz2], '.', label = "release")
        plt.plot([self.attr.flThrTop.t2, self.attr.flThrTop.t2, self.attr.flThrTop.t2], [self.attr.flThrTop.gx2, self.attr.flThrTop.gy2, self.attr.flThrTop.gz2], '.', label = "flThrTop")
        #plt.legend()
        plt.xlabel("time[ms]")
        plt.ylabel("gyro by mpu6050[deg/s] (elbow)")

        plt.subplot(224)
        plt.plot(self.t2, self.ax2, label = "x")
        plt.plot(self.t2, self.ay2, label = "y")
        plt.plot(self.t2, self.az2, label = "z")
        plt.plot([self.attr.pushAway.t2, self.attr.pushAway.t2, self.attr.pushAway.t2], [self.attr.pushAway.ax2, self.attr.pushAway.ay2,self.attr.pushAway.az2], '.', label = "pushAway")
        plt.plot([self.attr.downSwing1.t2, self.attr.downSwing1.t2, self.attr.downSwing1.t2], [self.attr.downSwing1.ax2, self.attr.downSwing1.ay2, self.attr.downSwing1.az2], '.', label = "downSwing")
        plt.plot([self.attr.backSwingBtm.t2, self.attr.backSwingBtm.t2, self.attr.backSwingBtm.t2], [self.attr.backSwingBtm.ax2, self.attr.backSwingBtm.ay2, self.attr.backSwingBtm.az2], '.', label = "backSwingBtm")
        plt.plot([self.attr.backSwingTop.t2, self.attr.backSwingTop.t2, self.attr.backSwingTop.t2], [self.attr.backSwingTop.ax2, self.attr.backSwingTop.ay2, self.attr.backSwingTop.az2], '.', label = "backSwingTop")
        plt.plot([self.attr.fwdSwingBtm.t2, self.attr.fwdSwingBtm.t2, self.attr.fwdSwingBtm.t2], [self.attr.fwdSwingBtm.ax2, self.attr.fwdSwingBtm.ay2, self.attr.fwdSwingBtm.az2], '.', label = "fwdSwingBtm")
        plt.plot([self.attr.release.t2, self.attr.release.t2, self.attr.release.t2], [self.attr.release.ax2, self.attr.release.ay2, self.attr.release.az2], '.', label = "release")
        plt.plot([self.attr.flThrTop.t2, self.attr.flThrTop.t2, self.attr.flThrTop.t2], [self.attr.flThrTop.ax2, self.attr.flThrTop.ay2, self.attr.flThrTop.az2], '.', label = "flThrTop")
        plt.legend(loc='upper left', bbox_to_anchor=(1,1))
        plt.xlabel("time[ms]")
        plt.ylabel("acc by mpu6050[g] (elbow)")
        '''

        plt.rcParams["figure.figsize"] = (18.5, 10.5)
        plt.suptitle(self.filename.replace(".txt", ""), fontsize = 25)

        #plt.clf()

    def plot_save(self):

        self.plot()
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        plt.savefig("{pB}/pybo/plot/{name}.png".format(pB = "./static", name = "currentplot"), dpi = 150)
        plt.clf()



#양 끝의 html tag 지우고 data 의 2X2 배열 반환
def GetDataFromHTML(html):
    data = html.split('\n')
    data.pop(0)
    data.pop(0)
    data.pop(0)
    data.pop(-1)
    data.pop(-1)
    for i in range(len(data)):
        data[i] = data[i].split('\t')

    return data


#str 배열에서 numpy array 반환
def ToNumpy(strAry):
    return list(map(float, strAry))


def GetData(url):

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text

    data = GetDataFromHTML(html)

    l = range(len(data))

    t = [data[i][0] for i in l]
    gx = [data[i][1] for i in l]
    gy = [data[i][2] for i in l]
    gz = [data[i][3] for i in l]

    ax = [data[i][4] for i in l]
    ay = [data[i][5] for i in l]
    az = [data[i][6] for i in l]

    '''
    mx = [data[i][7] for i in l]
    my = [data[i][8] for i in l]
    mz = [data[i][9] for i in l]

    t1 = [data[i][7] for i in l]

    gx1 = [data[i][8] for i in l]
    gy1 = [data[i][9] for i in l]
    gz1 = [data[i][10] for i in l]

    ax1 = [data[i][11] for i in l]
    ay1 = [data[i][12] for i in l]
    az1 = [data[i][13] for i in l]
    '''


    #mpu 9250의 gyro, 가속도, 자기장
    t = ToNumpy(t)

    gx = ToNumpy(gx)
    gy = ToNumpy(gy)
    gz = ToNumpy(gz)

    ax = ToNumpy(ax)
    ay = ToNumpy(ay)
    az = ToNumpy(az)

    '''
    mx = ToNumpy(mx)
    my = ToNumpy(my)
    mz = ToNumpy(mz)

    #mpu 6050의 gyro, 가속도
    t1 = ToNumpy(t1)

    gx1 = ToNumpy(gx1)
    gy1 = ToNumpy(gy1)
    gz1 = ToNumpy(gz1)

    ax1 = ToNumpy(ax1)
    ay1 = ToNumpy(ay1)
    az1 = ToNumpy(az1)
    '''

    return [t, gx, gy, gz, ax, ay, az]
    #return [t, gx, gy, gz, ax, ay, az, mx, my, mz, t1, gx1, gy1, gz1, ax1, ay1, az1]




def MainSwingCheck(loc_url, loc_pathBase, question_name):
    mainData = GetData(loc_url)    #로컬 서버에 올라온 html file에서 데이터 받아와서 SwingData1 객체 형성
    mainTime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    #mainDataType = 'ss'    #SwingData1에서 Type component 없앰
    mainFilename = question_name + mainTime + ".txt"
    mainSwingData = SwingData1(mainFilename, mainData, loc_pathBase)

    checklist = {'check1': mainSwingData.attr.elbowCheck, 'check2': mainSwingData.attr.dampCheck, 'check3': mainSwingData.attr.vibCheck, 'check4': mainSwingData.attr.backAngCheck, 'check5': mainSwingData.attr.rlTimeCheck, 'check6': mainSwingData.attr.rlAngCheck}   #1이 좋은 거임, 마지막은 ms(정수), float

    return checklist, mainSwingData
