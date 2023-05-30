import random
import time
from urllib import request
from selenium.webdriver.common.by import By
from .Login import LoginChromeWebdriverPlus
import sys
from Utils import SpiderUtils 
#sys.path.append("..") 
#import SpiderUtils

class JD(LoginChromeWebdriverPlus):
    """Summary of class here.

    继承LoginChromeWebdriverPlus父类实现京东滑块验证自动登录

    """

    def __init__(self,UserName,Password,Retry_times,LoginUrl):
        #初始化父类信息
        LoginChromeWebdriverPlus.__init__(self,UserName,Password,Retry_times)
        #初始化要登录的界面url
        self.LoginUrl = LoginUrl

    def login(self):
        """
        重写父类login函数实现京东网页登录
        """
        driver = self.driver
        driver.get(self.LoginUrl)

        #切换账号密码登录
        driver.find_element(By.CLASS_NAME,'login-tab-r').find_element(By.TAG_NAME,'a').click()
        # 设置账号密码
        SpiderUtils.LoginUtils.send_keys_interval(self.driver.find_element(By.ID,'loginname'), self.UserName)
        SpiderUtils.LoginUtils.send_keys_interval(self.driver.find_element(By.ID,'nloginpwd'), self.Password)
        time.sleep(random.random())
        #登录
        driver.find_element(By.ID,'loginsubmit').click()
        time.sleep(random.randint(1, 3))
        #获取滑块在整个电脑屏幕上的像素位置
        (SLIDE_X_POSITION,SLIDE_Y_POSITION) = SpiderUtils.SlideUtils.GetLocation(driver,'.JDJRV-slide-inner.JDJRV-slide-btn')
        
        #开始进行登录
        for i in range(self.Retry_times):
            time.sleep(1)
            # 获取验证码图片
            # 用于找到登录图片的大图
            try:
                background = driver.find_element(By.XPATH,r'//div/div[@class="JDJRV-bigimg"]/img')
            except:
                # 未查找到登陆图片则认为成功
                self.login_success = True
                
                break

            # 用来找到登录图片的小滑块
            slide = driver.find_element(By.XPATH,r'//div/div[@class="JDJRV-smallimg"]/img')
            background_url = background.get_attribute("src")
            slide_url = slide.get_attribute("src")
            background_img = 'images/background_img.png'
            slide_img = 'images/slide_img.png'
            # 下载背景大图保存到本地
            request.urlretrieve(background_url, background_img)
            # 下载滑块保存到本地
            request.urlretrieve(slide_url, slide_img)
            # 获取最佳x偏移量
            x = SpiderUtils.SlideUtils.find_pic(background_img, slide_img,'images/out.jpg')
            print(f'本地最佳偏移量: {x}')

            """
            可能有时候需要获得实际最佳偏移量
            """
            
            """
            # 计算缩放
            # 获取下载背景图宽度
            w1 = cv2.imread(background_img).shape[1]
            # 获取网页背景图宽度
            w2 = background.size['width']
            # 计算实际页面x偏移量
            y = x * w2 / w1
            print(f'实际最佳偏移量: {y}')
            """

            #设置偏移值
            offset = x
            """
            其中SLIDE_X_POSITION为屏幕左上角至滑块中心的横向像素值,SLIDE_Y_POSITION为屏幕左上角至滑块中心纵向像素值
            不同屏幕该值是不同的,通过函数VerifyLoginUtils.SlideUtils.GetLocation获得
            """

            #进行滑块验证
            SpiderUtils.SlideUtils.slide_by_autogui(SLIDE_X_POSITION, SLIDE_Y_POSITION, offset)


