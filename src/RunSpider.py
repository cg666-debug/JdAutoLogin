import Login_Accomplish.JdLogin
import Utils.SpiderUtils
import os
import sys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


path = os.path.realpath(sys.argv[0])
# 读取配置文件

#获取当前代码执行的路径
#DIR = sys.path[0]

#SettingPath = os.path.join(DIR,'setting.yaml')
SettingPath = './setting/setting.yaml'
#SettingPath = os.path.join(os.path.dirname(path),'setting.yaml')
ConfigInfo = Utils.SpiderUtils.PublicUtils.ReadSetting(SettingPath)
LoginInfo = ConfigInfo['login']

JD = Login_Accomplish.JdLogin.JD(LoginInfo['UserName'],LoginInfo['PassWord'],LoginInfo['Retry_times'],LoginInfo['LoginUrl'])
JD.login()
driver = JD.get_driver()

#等待跳转到京东主页面
WebDriverWait(driver, 120).until(EC.url_to_be(LoginInfo['MainUrl']))

#运行爬虫


