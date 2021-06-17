# -*- coding: utf-8 -*-
"""
SwingAttribute class 정의하는 파일
SwingData1(mag 포함) class 정의하는 파일과 같은 폴더에 있어야 될 거 같음?! 모르겠다..
"""

'''
import matplotlib.pyplot as plt

# title 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
#font_path = "C:/Windows/Fonts/NGULIM.TTF"
font_path = "C:/Users/hp/AppData/Local/Microsoft/Windows/Fonts/NotoSansCJKkr-Regular.otf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
'''

def slope(dataArr, timeArr, i):

    slope = dataArr[i+1] - dataArr[i]
    dt = timeArr[i+1] - timeArr[i]
    slope = slope / dt

    return slope


def curv(dataArr, timeArr, i):

    slope1 = slope(dataArr, timeArr, i)
    slope2 = slope(dataArr, timeArr, i+1)
    dt = timeArr[i+1] - timeArr[i]

    k = (slope2 - slope1) / dt

    return k



class SwingDataPoint:

    '''
    SwingData array((1+6) * (timestep+1))에서
    특정 index에서의 t1, gx1, ..., az1 값
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
        #self.mx = swingdata.mx[index]
        #self.my = swingdata.my[index]
        #self.mz = swingdata.mz[index]
        # self.p1 = swingdata.p1[index]    # pitch, roll, yaw 추가
        # self.r1 = swingdata.r1[index]
        # self.y1 = swingdata.y1[index]

        #self.t2 = swingdata.t2[index]
        #self.gx2 = swingdata.gx2[index]
        #self.gy2 = swingdata.gy2[index]
        #self.gz2 = swingdata.gz2[index]
        #self.ax2 = swingdata.ax2[index]
        #self.ay2 = swingdata.ay2[index]
        #self.az2 = swingdata.az2[index]
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

        self.istest = True

        '''

        ************************************
        test용 데이터는 아랫줄 주석 풀고 사용!!
        ************************************

        '''

        self.istest = True    #test용 데이터 아닌 경우 주석처리!!!

        self.swingData = swingData    #SwingData1 class

        # SwingAttribute[1]~[8]: phases
        #self.pushAway = self.pushAwayPoint()
        self.downSwing1 = self.downSwingPoint(10, 1)
        #self.downSwing2 = self.downSwingPoint(self.pushAway.index, 2)
        self.backSwingBtm = self.backSwingBtmPoint(self.downSwing1.index)
        self.backSwingTop = self.backSwingTopPoint(self.backSwingBtm.index)
        self.fwdSwingBtm = self.fwdSwingBtmPoint(self.backSwingTop.index)
        self.release = self.releasePoint(self.backSwingTop.index)
        self.flThrTop = self.flThrTopPoint(self.fwdSwingBtm.index)  # release는 정확하게 알 수 없다고 가정하고, fwdSwingBtm을 latestIndex로 사용
        #self.flThrDamp = self.flThrDampRatio(self.flThrTop.index) # 비어있음... 0

        self.elbowCheck = self.elbowCheckFn()

        # vibCheck에 값 필요해서 먼저 계산
        self.rlTimeCheck = self.rlTimeCheckFn()

        self.dampCheck = self.dampCheckFn()
        self.vibCheck = self.vibCheckFn()
        self.backAngCheck = self.backAngCheckFn()
        self.rlAngCheck = self.rlAngCheckFn()



    '''
    def pushAwayPoint(self):

        #1. pushAway: 팔꿈치를 앞으로 조금 밀기 시작하는 순간
        #= gx2>0, gz2<0으로 두 값의 차이가 ths 값을 넘었을 때


        ths = 10.0    # gyro (단위 deg/s)
        pushAwayIndex = 0

        for i in range(len(self.swingData.t1)):
            pushAwayIndex += 1
            if (self.swingData.gx2[i] - self.swingData.gz2[i] > ths):
                break

        pushAwayPoint = SwingDataPoint(self.swingData, pushAwayIndex)

        return pushAwayPoint
    '''

    def downSwingPoint(self, latestIndex, loc):

        if self.istest:
            downSwingPoint = SwingDataPoint(self.swingData, 100)
            return downSwingPoint
        '''
        2. downSwing:
            - loc = 1 (손목이) 백스윙 시작하는 순간 = gy1>ths
        '''

        ths = 30.0    # gyro (단위 deg/s)
        downSwingIndex = latestIndex

        if loc == 1:
            for i in range(downSwingIndex, len(self.swingData.t1)-1):
                downSwingIndex += 1
                if (self.swingData.gy1[i] > ths):
                    break
        '''
        elif loc == 2:
            for i in range(downSwingIndex, len(self.swingData.t1)):
                downSwingIndex += 1
                if (self.swingData.gy2[i] > ths):
                    break
        '''

        downSwingPoint = SwingDataPoint(self.swingData, downSwingIndex)

        return downSwingPoint

    def backSwingBtmPoint(self, latestIndex):

        if self.istest:
            backSwingBtmPoint = SwingDataPoint(self.swingData, 150)
            return backSwingBtmPoint
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

        if self.istest:
            backSwingTopPoint = SwingDataPoint(self.swingData, 150)
            return backSwingTopPoint

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

        if self.istest:
            fwdSwingBtmPoint = SwingDataPoint(self.swingData, 200)
            return fwdSwingBtmPoint

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

        if self.istest:
            releasePoint = SwingDataPoint(self.swingData, 250)
            return releasePoint

        '''
        6. release: 공을 놓는 시점
        az +값으로 크게 발생하는 지점: 앞으로 손을 털기 때문에 발생
        release point가 잘 보이지 않을 수 있음: 공을 잘 놓지 못한 것 => index = 501? 500?
        '''

        ths = 2.7    # 가속도 (단위 g)
        releaseIndex = latestIndex

        for i in range(releaseIndex, len(self.swingData.t1)-1):
            if (self.swingData.az1[i] > ths):
                break
            releaseIndex += 1

        releasePoint = SwingDataPoint(self.swingData, releaseIndex)

        return releasePoint


    def flThrTopPoint(self, latestIndex):

        if self.istest:
            flThrTopPoint = SwingDataPoint(self.swingData, 300)
            return flThrTopPoint

        '''
        7. flwThrTop: 팔로우 스루 중 최고점 = gy1 = 0
        '''

        #ths = 10.0    # 각가속도 (단위 deg/s)
        flThrTopIndex = latestIndex

        for i in range(flThrTopIndex, len(self.swingData.t1)-2):
            flThrTopIndex += 1
            if (self.swingData.gy1[i] * self.swingData.gy1[i+1] < 0):
                break

        flThrTopPoint = SwingDataPoint(self.swingData, flThrTopIndex)

        return flThrTopPoint

    """--------------------Checklist Fn---------------------"""

    def elbowCheckFn(self):
        """
        elbowCheckResult = 1

        backSwingSlice = 30
        backSwingGy1 = self.swingData.gy1[self.downSwing1.index : self.backSwingTop.index]
        backSwingLen = len(backSwingGy1)

        avg = 0.0
        ths = 1.0
        #indexj = 0
        count = 0

        for i in range(backSwingSlice):
            avg = (backSwingGy1[2*i] + backSwingGy1[backSwingLen - 2*i - 1])/2.0
            for j in range(2*i+6, backSwingLen - 2*i - 7):
                #indexj = j
                if abs(backSwingGy1[j] - avg) < ths:
                    count += 1
                    #elbowCheckResult = backSwingGy1[j] - avg

                    #break
            #if elbowCheckResult == 0:
            #    break
        """
        count = 1
        return count


        '''
        backSwingIndex = list(range(self.downSwing1.index, self.backSwingTop.index))
        backSwingGy1 = self.swingData.gy1[self.downSwing1.index : self.backSwingTop.index]

        backSwingCurv = []
        backSwingIndex.pop(1)

        for i in backSwingIndex:
            k = curv(self.swingData.gy1, self.swingData.t1, i)
            backSwingCurv.append(k)

        return backSwingCurv
        '''

        '''
        backSwinglenHalf = len(range(self.downSwing1.index, self.backSwingTop.index))//2

        backSwingGy1_1 = self.swingData.gy1[self.downSwing1.index : self.downSwing1.index + backSwinglenHalf]
        backSwingGy1_2 = self.swingData.gy1[self.downSwing1.index + backSwinglenHalf : self.backSwingTop.index]

        gy1max1index = self.downSwing1.index + backSwingGy1_1.index(max(backSwingGy1_1))
        gy1max2index = self.downSwing1.index + backSwingGy1_2.index(max(backSwingGy1_2))

        backSwingV = self.swingData.gy1[gy1max1index : gy1max2index]

        backSwingVmin = max(backSwingGy1_1)
        if len(backSwingV) != 0 :
            backSwingVmin = min(backSwingV)

        backSwingVdif = min(max(backSwingGy1_1) - backSwingVmin, max(backSwingGy1_2) - backSwingVmin)
        '''

        return 0
        #return elbowCheckResult


    def dampCheckFn(self):
        '''
        힘을 빼고 스윙을 했는가? = flThrTop 이후에도 자연스럽게 스윙이 이어졌는가?
        flThrTop 이후 gy1 = 0인 지점 2개 찾기
        두 지점 사이에 진동 진폭 구하기 (max, min of gy1)
        => 첫 번째 진폭의 크기가 충분한가?
        => 두 번째 진폭의 크기가 첫 번째의 1/2보다 큰가?
        둘 다 만족하면 1(좋음), 하나라도 만족 안 하면 0(안 좋)
        '''
        dampCheckResult = 0
        datalen = len(self.swingData.gy1)

        zeroIndex1 = self.flThrTop.index + 5
        iszero1 = 0

        for i in list(range(self.flThrTop.index + 5, datalen - 10)):
            if (self.swingData.gy1[i]*self.swingData.gy1[i+1] < 0):
                iszero1 = 1
                break
            zeroIndex1 += 1

        # 첫 번째 zero 점 못 찾았다면 힘 빼지 않아서 잔여 스윙이 충분하지 않은 것으로 판단
        if iszero1 == 0:
            return dampCheckResult

        zeroIndex2 = zeroIndex1 + 5
        iszero2 = 0

        for i in list(range(zeroIndex1 + 5,datalen - 1)):
            if (self.swingData.gy1[i]*self.swingData.gy1[i+1] < 0):
                iszero2 = 1
                break
            zeroIndex2 += 1

        # 두 번째 zero 점 못 찾았다면 힘 빼지 않아서 잔여 스윙이 충분하지 않은 것으로 판단
        if iszero2 == 0:
            return dampCheckResult

        # 진폭 계산
        amp1 = max(self.swingData.gy1[self.flThrTop.index : zeroIndex1])
        amp2 = min(self.swingData.gy1[zeroIndex1 : zeroIndex2])

        # 첫 번째 진폭의 크기가 충분한가?
        ths1 = 200.0
        if amp1 < ths1:
            #return dampCheckResult
            return [dampCheckResult, zeroIndex1, zeroIndex2, amp1, amp2]

        # 두 번째 진폭의 크기가 첫 번째와 비교했을 때 충분한가?
        ths2 = 0.35
        if abs(amp2 / amp1) < ths2:
            #return dampCheckResult
            return [dampCheckResult, zeroIndex1, zeroIndex2, amp1, amp2]

        dampCheckResult = 1
        return [dampCheckResult, zeroIndex1, zeroIndex2, amp1, amp2]


    def vibCheckFn(self):

        ay1var = 0.0  #gy

        return 0


    def backAngCheckFn(self):

        return 0


    def rlTimeCheckFn(self):
        '''
        fwdSwingBtm.t1과 release.t1의 차이 = rlTime (단위: ms) 반환
        releasePoint()에서 확실한 release point 알 수 없으면 release 시점이 맨끝에 잡히고,
        이런 경우 또는 이상한 점에 release point가 특정될 경우를 구분하기 위해
        ths보다 rlTime이 크면 특정 시간 반환: 3000
        '''

        rlTime = self.fwdSwingBtm.t1 - self.release.t1
        # 양수 -> release 이후 최하점 / 음수 -> 최하점 이후 release

        '''
        ths = 500   # fwdSwingBtm과 release 차이가 비정상적으로 클 경우 (점이 잘 안 찍힌 경우)
        if abs(rlTime) > ths:
            rlTime = 3000   # rlTime이 잘 계산되지 않았을 때 반환할 특정한 값
        '''

        return rlTime


    def rlAngCheckFn(self):

        return 0.0



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