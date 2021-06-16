# -*- coding: utf-8 -*-
"""
SwingAttribute class 정의하는 파일
SwingData1(mag 포함) class 정의하는 파일과 같은 폴더에 있어야 될 거 같음?! 모르겠다..
"""


import matplotlib.pyplot as plt

"""
# title 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
#font_path = "C:/Users/hp/AppData/Local/Microsoft/Windows/Fonts/NotoSansCJKkr-Regular.otf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
"""

def slope(dataArr, timeArr, i):

    slope = dataArr[i+1] - dataArr[i]
    dt = timeArr[i+1] - timeArr[i]
    slope = slope / dt

    return slope


def mid(dataArr, i):
    mid = (dataArr[i+1] + dataArr[i]) / 2
    return mid



class SwingDataPoint:

    '''
    SwingData array((1+6+1+6) * (timestep+1))에서
    특정 index에서의 t1, gx1, ..., az2 값
    '''

    def __init__(self, swingdata, index):    #swingdata는 SwingData1 type

        self.index = index

        self.t1 = swingdata.t1[index]
        self.gx1 = swingdata.gx1[index]
        self.gy1 = swingdata.gy1[index]
        self.gz1 = swingdata.gz1[index]
        self.ax1 = swingdata.ax1[index]
        self.ay1 = swingdata.ay1[index]
        self.az1 = swingdata.az1[index]
        self.mx = swingdata.mx[index]
        self.my = swingdata.my[index]
        self.mz = swingdata.mz[index]
        # self.p1 = swingdata.p1[index]    # pitch, roll, yaw 추가
        # self.r1 = swingdata.r1[index]
        # self.y1 = swingdata.y1[index]

        self.t2 = swingdata.t2[index]
        self.gx2 = swingdata.gx2[index]
        self.gy2 = swingdata.gy2[index]
        self.gz2 = swingdata.gz2[index]
        self.ax2 = swingdata.ax2[index]
        self.ay2 = swingdata.ay2[index]
        self.az2 = swingdata.az2[index]
        # self.p2 = swingdata.p2[index]
        # self.r2 = swingdata.r2[index]
        # self.y2 = swingdata.y2[index]


class SwingAttribute:

    '''
    Swing의 각 지점의 index를 각 함수로 받아서 SwingDataPoint 형태로 저장

    1. pushAway: 팔꿈치를 앞으로 조금 밀기 시작하는 순간 = gx2>0, gz2<0으로 두 값의 차이가 ths 값을 넘었을 때
    2. backSwing:
    - 1(손목이) 백스윙을 시작하는 순간 = gy1>0으로 ths 값을 넘었을 때
    - 2(팔꿈치가) 백스윙을 시작하는 순간 = gy2>0으로 ths 값을 넘었을 때
    3. backSwingBtm: 백스윙 중 최저점 = gy1이 증가  감소로 기울기 0 될 때
    4. backSwingTop: 백스윙탑; 백스윙 중 최고점
    - 가속도 그래프: X축 가속도가 negative이 된 후 0인 시점(y,z도 0) 이 백스윙탑
    - 각속도 그래프: 사실 원래대로 각속도가 0인 지점(속도가 0)이 백스윙탑
    5. fwdSwingBtm: 포워드 스윙 중 최저점 = gy1 최저점
    6. release: 공을 놓는 시점 = *코치님 데이터에서 y축 가속도 발생하는(negative값) 지점이 릴리스 포인트* (확실치는 X?)
    7. flThrTop: 팔로우 스루 중 최고점 = gy1 = 0
    8. flThrDamp: 팔로우 스루 중 잔여 스윙? 작은 것이 좋고(힘이 잘 빠졌다는 뜻) 너무 작으면 인위적으로 스윙을 한 것일 수 있으므로 적당한 범위 내일 때 좋다고 판단해야 할 것 같다.

    '''


    def __init__(self, swingData):

        self.swingData = swingData    #SwingData1 class

        # SwingAttribute[1]~[8]: phases
        self.pushAway = self.pushAwayPoint()
        self.downSwing1 = self.downSwingPoint(self.pushAway.index, 1)
        self.downSwing2 = self.downSwingPoint(self.pushAway.index, 2)
        self.backSwingBtm = self.backSwingBtmPoint(self.downSwing1.index)
        self.backSwingTop = self.backSwingTopPoint(self.backSwingBtm.index)
        self.fwdSwingBtm = self.fwdSwingBtmPoint(self.backSwingTop.index)
        self.release = self.releasePoint(self.fwdSwingBtm.index)
        self.flThrTop = self.flThrTopPoint(self.fwdSwingBtm.index)  # release는 정확하게 알 수 없다고 가정하고, fwdSwingBtm을 latestIndex로 사용
        self.flThrDamp = self.flThrDampRatio(self.flThrTop.index) # 비어있음... 0

        self.elbowCheck = self.elbowCheckFn()
        self.dampCheck = self.dampCheckFn()




    def pushAwayPoint(self):
        '''
        1. pushAway: 팔꿈치를 앞으로 조금 밀기 시작하는 순간
        = gx2>0, gz2<0으로 두 값의 차이가 ths 값을 넘었을 때
        '''

        ths = 10.0    # gyro (단위 deg/s)
        pushAwayIndex = 0

        for i in range(len(self.swingData.t1)):
            pushAwayIndex += 1
            if (self.swingData.gx2[i] - self.swingData.gz2[i] > ths):
                break

        pushAwayPoint = SwingDataPoint(self.swingData, pushAwayIndex)

        return pushAwayPoint

    def downSwingPoint(self, latestIndex, loc):

        '''
        2. backSwing:
            - loc = 1 (손목이) 백스윙 시작하는 순간 = gy1>ths
            - loc = 2 (팔꿈치가) 백스윙 시작하는 순간 = gy2>ths
        '''

        ths = 20.0    # gyro (단위 deg/s)
        downSwingIndex = latestIndex

        if loc == 1:
            for i in range(downSwingIndex, len(self.swingData.t1)):
                downSwingIndex += 1
                if (self.swingData.gy1[i] > ths):
                    break
        elif loc == 2:
            for i in range(downSwingIndex, len(self.swingData.t1)):
                downSwingIndex += 1
                if (self.swingData.gy2[i] > ths):
                    break

        downSwingPoint = SwingDataPoint(self.swingData, downSwingIndex)

        return downSwingPoint

    def backSwingBtmPoint(self, latestIndex):
        '''
        3. backSwingBtm: 백스윙 중 최저점 = gy1이 증가 -> 감소로 기울기 0 될 때
        '''

        backSlice = 100   # 최소값 찾을 범위 timestep 길이
        backSwingBtmIndex = latestIndex
        backSwingGy1 = self.swingData.gy1[backSwingBtmIndex : backSwingBtmIndex + backSlice]
        backSwingBtmIndex += backSwingGy1.index(max(backSwingGy1))

        '''
        ths = 20.0    # 각가속도 (단위 deg/1000s^2)
        backSwingBtmIndex = latestIndex

        for i in range(backSwingBtmIndex, len(self.swingData.t1)):
            backSwingBtmIndex += 1
            if (abs(slope(self.swingData.gy1, self.swingData.t1, i)) < ths):
                break
        '''

        backSwingBtmPoint = SwingDataPoint(self.swingData, backSwingBtmIndex)

        return backSwingBtmPoint

    def backSwingTopPoint(self, latestIndex):
        '''
        4. backSwingTop: 백스윙탑; 백스윙 중 최고점
        - 가속도 그래프: X축 가속도가 negative이 된 후 0인 시점(y,z도 0) 이 백스윙탑
        *일단 이걸로* - 각속도 그래프: 사실 원래대로 각속도가 0인 지점(속도가 0)이 백스윙탑
        =>수정: i번째 값 * i+1번째 값 < 0
        '''

        #ths = 10.0    # gyro (단위 deg/s)
        backSwingTopIndex = latestIndex

        for i in range(backSwingTopIndex, len(self.swingData.t1)):
            backSwingTopIndex += 1
            if (self.swingData.gy1[i] * self.swingData.gy1[i+1] < 0):
                break

        backSwingTopPoint = SwingDataPoint(self.swingData, backSwingTopIndex)

        return backSwingTopPoint

    def fwdSwingBtmPoint(self, latestIndex):
        '''
        5. fwdSwingBtm: 포워드 스윙 중 최저점 = gy1 최저점
        '''

        fwdSlice = 60   # 최소값 찾을 범위 timestep 길이
        fwdSwingBtmIndex = latestIndex

        fwdSwingGy1 = self.swingData.gy1[fwdSwingBtmIndex : fwdSwingBtmIndex + fwdSlice]
        fwdSwingBtmIndex += fwdSwingGy1.index(min(fwdSwingGy1))

        fwdSwingBtmPoint = SwingDataPoint(self.swingData, fwdSwingBtmIndex)

        return fwdSwingBtmPoint

    def releasePoint(self, latestIndex):
        '''
        6. release: 공을 놓는 시점
        = 코치님 데이터에서 y축 가속도 발생하는(negative값) 지점이 릴리스 포인트
        (확실치는 X?)
        '''

        ths = -0.3    # 가속도 (단위 g)
        releaseIndex = latestIndex

        for i in range(releaseIndex, len(self.swingData.t1)):
            releaseIndex += 1
            if (self.swingData.ay1[i] < ths):
                break

        releasePoint = SwingDataPoint(self.swingData, releaseIndex)

        return releasePoint

    def flThrTopPoint(self, latestIndex):
        '''
        7. flwThrTop: 팔로우 스루 중 최고점 = gy1 = 0
        '''

        #ths = 10.0    # 각가속도 (단위 deg/s)
        releaseIndex = latestIndex

        for i in range(releaseIndex, len(self.swingData.t1)):
            releaseIndex += 1
            if (self.swingData.gy1[i] * self.swingData.gy1[i+1] < 0):
                break

        releasePoint = SwingDataPoint(self.swingData, releaseIndex)

        return releasePoint

    def flThrDampRatio(self, latestIndex):

        return 0

    def elbowCheckFn(self):
        elbowCheckResult = 1
        backSwingindex = range(self.downSwing1.index, self.backSwingTop.index)

        for i in backSwingindex:
            pass

        return elbowCheckResult



'''
    def plot(self):

        """
    스윙 단계별 위치를 SwingData1 plot 위에 표시
    1. pushAway: 팔꿈치를 앞으로 조금 밀기 시작하는 순간 = gx2>0, gz2<0으로 두 값의 차이가 ths 값을 넘었을 때
    2. backSwing:
    - 1(손목이) 백스윙을 시작하는 순간 = gy1>0으로 ths 값을 넘었을 때
    - 2(팔꿈치가) 백스윙을 시작하는 순간 = gy2>0으로 ths 값을 넘었을 때
    3. backSwingBtm: 백스윙 중 최저점 = gy1이 증가  감소로 기울기 0 될 때
    4. backSwingTop: 백스윙탑; 백스윙 중 최고점
    - 가속도 그래프: X축 가속도가 negative이 된 후 0인 시점(y,z도 0) 이 백스윙탑
    - 각속도 그래프: 사실 원래대로 각속도가 0인 지점(속도가 0)이 백스윙탑
    5. fwdSwingBtm: 포워드 스윙 중 최저점 = gy1 최저점
    6. release: 공을 놓는 시점 = *코치님 데이터에서 y축 가속도 발생하는(negative값) 지점이 릴리스 포인트* (확실치는 X?)
    7. flThrTop: 팔로우 스루 중 최고점 = gy1 = 0
    8. flThrDamp: 팔로우 스루 중 잔여 스윙? 작은 것이 좋고(힘이 잘 빠졌다는 뜻) 너무 작으면 인위적으로 스윙을 한 것일 수 있으므로 적당한 범위 내일 때 좋다고 판단해야 할 것 같다.
        """

        plt.subplot(231)
        plt.plot(self.pushAway.t1, self.pushAway.gx1, label = "pushAway")
        plt.plot(self.pushAway.t1, self.pushAway.gy1, label = "pushAway")
        plt.plot(self.pushAway.t1, self.pushAway.gz1, label = "pushAway")
        plt.plot(self.downSwing1.t1, self.downSwing1.gx1, label = "downSwing")
        plt.plot(self.downSwing1.t1, self.downSwing1.gy1, label = "downSwing")
        plt.plot(self.downSwing1.t1, self.downSwing1.gz1, label = "downSwing")
        plt.plot(self.backSwingBtm.t1, self.backSwingBtm.gx1, label = "backSwingBtm")
        plt.plot(self.backSwingBtm.t1, self.backSwingBtm.gy1, label = "backSwingBtm")
        plt.plot(self.backSwingBtm.t1, self.backSwingBtm.gz1, label = "backSwingBtm")
        plt.plot(self.backSwingTop.t1, self.backSwingTop.gx1, label = "backSwingTop")
        plt.plot(self.backSwingTop.t1, self.backSwingTop.gy1, label = "backSwingTop")
        plt.plot(self.backSwingTop.t1, self.backSwingTop.gz1, label = "backSwingTop")
        plt.plot(self.fwdSwingBtm.t1, self.fwdSwingBtm.gx1, label = "fwdSwingBtm")
        plt.plot(self.fwdSwingBtm.t1, self.fwdSwingBtm.gy1, label = "fwdSwingBtm")
        plt.plot(self.fwdSwingBtm.t1, self.fwdSwingBtm.gz1, label = "fwdSwingBtm")
        plt.plot(self.release.t1, self.release.gx1, label = "release")
        plt.plot(self.release.t1, self.release.gy1, label = "release")
        plt.plot(self.release.t1, self.release.gz1, label = "release")
        plt.plot(self.flThrTop.t1, self.flThrTop.gx1, label = "flThrTop")
        plt.plot(self.flThrTop.t1, self.flThrTop.gy1, label = "flThrTop")
        plt.plot(self.flThrTop.t1, self.flThrTop.gz1, label = "flThrTop")

        #plt.subplot(232)

        #plt.subplot(233)

        #plt.subplot(234)

        #plt.subplot(235)

        plt.rcParams["figure.figsize"] = (18.5, 10.5)
        #plt.clf()
'''

'''
    def plot_save(self):

        self.plot()
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        plt.savefig("{pB}/plot/{T}/{name}.png".format(pB = pathBase, T = self.Type, name = self.filename.replace(".txt", "")), dpi = 150)
        plt.clf()
'''