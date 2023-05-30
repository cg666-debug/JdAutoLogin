import cv2
import pyautogui
import random
import time
import os
import sys
import datetime
import requests
import json
import yaml
from selenium.webdriver.common.by import By
from pprint import pprint

"""
自动登录页面然后进行爬虫所需的基本工具类和函数
"""

class SlideUtils:
    """Summary of class here.

    滑块验证工具类

    methods:
        find_pic(bg,tp,out): 用于找出背景图片中的滑块缺口的位置
        slide_by_autogui(x,y,offset): 根据滑块的位置以及缺口偏差值完成滑动
        GetLocation(driver): 获取滑块坐标 
    """

    @staticmethod
    def find_pic(bg,tp,out):
        '''
        bg: 背景图片
        tp: 缺口图片
        out:输出图片
        '''
        # 读取背景图片和缺口图片
        bg_img = cv2.imread(bg) # 背景图片
        tp_img = cv2.imread(tp) # 缺口图片
        
        # 识别图片边缘
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)
        
        # 转换图片格式
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
        
        # 缺口匹配
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 寻找最优匹配
        
        # 绘制方框
        th, tw = tp_pic.shape[:2] 
        tl = max_loc # 左上角点的坐标
        br = (tl[0]+tw,tl[1]+th) # 右下角点的坐标
        cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # 绘制矩形
        cv2.imwrite(out, bg_img) # 保存在本地
        
        x = (tl[0]+br[0])/2
        return x

        # 返回缺口的X坐标
        #return tl[0]

    
    @staticmethod
    def slide_by_autogui(x, y, offset):
        """
        使用pyautogui实现滑块并自定义轨迹方程
        """
        xx = x + offset
        pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.mouseDown()
        y += random.randint(9, 19)
        pyautogui.moveTo(x + int(offset * random.randint(15, 23) / 20), y, duration=0.28)
        y += random.randint(-9, 0)
        pyautogui.moveTo(x + int(offset * random.randint(17, 21) / 20), y, duration=random.randint(20, 31) / 100)
        y += random.randint(0, 8)
        pyautogui.moveTo(xx, y, duration=0.3)
        pyautogui.mouseUp()

    
    @staticmethod
    def GetLocation(driver,FindPath):
        '''
        pyautogui操作的坐标是元素在整个电脑屏幕上的像素的位置

        driver返回的location是元素相对于网页界面左上角的尺寸位置

        所以需要进行两步转换，第一步将元素相对于网页界面的尺寸位置转换成相对于网页左上角的位置，第二步将尺寸位置转换成像素位置

        变量说明:
            driver: chromewebdriver
            
            FindPath: 利用driver.find_element通过By.CSS_SELECTOR查询的路径
        '''

        #获取拖动块的location
        #slide_button = driver.find_element(By.CSS_SELECTOR,'.JDJRV-slide-inner.JDJRV-slide-btn')
        slide_button = driver.find_element(By.CSS_SELECTOR,FindPath)
        print("滑块位置信息")
        print(slide_button.rect)

        #获取电脑屏幕的像素
        (windowx,windowy) = pyautogui.size()

        #获取屏幕尺寸信息
        screenx = driver.execute_script('return screen.width')
        screeny = driver.execute_script('return screen.height')

        #获取网页尺寸信息
        documentx = driver.execute_script('return document.documentElement.clientWidth')
        documenty = driver.execute_script('return document.documentElement.clientHeight')

        #重新计算滑块相对于整个屏幕上的位置，然后再计算出像素位置
        PositionX = (slide_button.rect['x']+screenx-documentx)*(windowx/screenx)
        PositionY = (slide_button.rect['y']+screeny-documenty)*(windowy/screeny)

        print("x: ",PositionX," y: ",PositionY)
        return (PositionX,PositionY)
    


class LoginUtils:
    """Summary of class here.

    登录工具类

    """
    @staticmethod
    def send_keys_interval(element, text, interval=0.1):
        """
        webdriver 模拟人输入文本信息
        """
        for c in text:
            element.send_keys(c)
            time.sleep(random.randint(int(interval * 500), int(interval * 1500)) / 1000)


class PublicUtils:
    """Summary of class here.

    公共工具类

    """

    @staticmethod
    def ReadSetting(SettingPath):
        """
        读取配置文件
        """
        with open(os.path.expanduser(SettingPath),"r") as config:
            cfg = yaml.safe_load(config)
        
        return cfg
    

    @staticmethod
    def make_print_to_file(fileName="Default.log",path=""):
        '''
        path,it is a path for save your log about fuction print
        example:
        use  make_print_to_file()   and the   all the information of funtion print , will be write in to a log file
        :return:
        '''
    
        class Logger(object):
            def __init__(self, filename, path):
                self.terminal = sys.stdout
                #self.path= os.path.join(path, filename)
                self.path = filename
                self.log = open(self.path, "w+", encoding='utf8',)
                print("save:", os.path.join(self.path, filename))
    
            def write(self, message):
                self.terminal.write(message)
                self.log.write(message)
    
            def flush(self):
                pass
    
    
    
    
        #fileName = datetime.datetime.now().strftime('day'+'%Y_%m_%d')
        sys.stdout = Logger(fileName, path)
    
        #############################################################
        # 这里输出之后的所有的输出的print 内容即将写入日志
        #############################################################
        #print(fileName.center(60,'*'))

