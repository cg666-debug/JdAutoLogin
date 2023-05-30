from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


class LoginChromeWebdriverPlus:
    """Summary of class here.

    使用selenium模拟登录,并实现一些基本的功能可供子类继承

    """

    def __init__(self,UserName,Password,Retry_times) :

        """
        初始化用户名,密码,登录页面,验证重试次数,chrome webdriver
        """

        #初始化webdriver

        #创建Chrome参数对象
        option = Options()
        # 随机User-Agent
        ua = UserAgent()
        a = ua.random
        user_agent = ua.random
        # 替换User-Agent
        option.add_argument(f'user-agent={user_agent}')

        #添加试验性参数
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        option.add_experimental_option('useAutomationExtension', False)
        # 创建Chrome浏览器对象并传入参数
        self.driver = webdriver.Chrome(options=option)
        # 执行Chrome开发者协议命令（在加载页面时执行指定的JavaScript代码）
        self.driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
        )
        self.driver.maximize_window()

        self.UserName = UserName
        self.Password = Password
        self.Retry_times = Retry_times
        self.login_success = False

    def is_login(self):
        """
        是否已登录成功 
        """
        return self.login_success

    def get_cookies(self):
        """
        获取webdriver cookies
        """
        return self.driver.get_cookies()

    def get_cookies_dict(self):
        """
        获取字典结构的cookie
        """
        cookies = self.get_cookies()
        res = {}
        for cookie in cookies:
            res[cookie['name']] = cookie['value']
        return res

    def get_driver(self):
        """
        获取webdriver对象
        """
        return self.driver

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()
    

    def login(self):
        """
        继承的子类重写该方法
        """
        pass