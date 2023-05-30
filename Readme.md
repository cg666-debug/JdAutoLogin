# 自动实现滑块验证登录京东 -- 彭立成 2023/5/29

==============================

### 一、环境依赖
- Anaconda version 1.7.2
- Python 3.7.0
- 根目录下requirements.txt

### 二、环境部署
在根目录下执行
```python
pip install -r requirements.txt
```

### 三、目录结构
```
|-- JdAutoLogin
    |-- Readme.md   帮助文档
    |-- requirements.txt    环境依赖 
    |-- src
        |-- main.py     定时任务入口文件
        |-- RunSpider.py    自动登录京东可添加后续爬虫代码
        |-- setting
            |-- setting.yaml    配置文件
        |-- Utils.py    工具类
            |--SpiderUtils.py   登录所需工具类和函数
        |-- chromedriver_win32      浏览器驱动
        |   |-- chromedriver.exe    
        |-- images      
        |   |-- background_img.png      滑块验证背景图
        |   |-- out.jpg     滑块缺口位置图
        |   |-- slide_img.png   滑块图
        |-- Login_Accomplish
        |   |-- JdLogin.py  继承基本类实现京东的登录
        |   |-- Login.py    登录基本类
```

### 四、项目启动
#### 1
根据需求更改setting.yaml配置文件
```yaml
login:
# UserName for logging in to the website
  UserName: 'xxxxx'
# PassWord for logging in to the website
  PassWord: 'xxxxx'
# The URL of the login page
  LoginUrl: 'https://passport.jd.com/uc/login'
# After login, go to the URL of the page
  MainUrl: 'https://www.jd.com/'
# Number of retries for slider validation
  Retry_times: 10
```

#### 2
- 运行定时任务（固定某个时间启动爬虫）
```python
python main.py
```
- 运行一次爬虫
```python
python RunSpider.py
```


### 五、项目打包
**如果对项目进行修改需要重新打包成exe**
- cd到RunSpider.py同级目录中执行
```
pyi-makespec RunSpider.py
```
- 配置RunSpider.spec文件，具体配置参数可查看[pyinstaller配置文件参数](https://blog.csdn.net/tangfreeze/article/details/112240342)
- 执行
```shell
pyinstaller RunSpider.spec
命令执行完后会生成build和dist文件夹

可能提示
ModuleNotFoundError: No module named 'fake_useragent.data'
```
- 使用手动添加fake-useragent（尝试配置spec自动添加无法成功）
    - 确定当前python环境中site-packages的位置
  ```shell
    python -m site
  ```
    - 将 **.../site-packages/fake-useragent**文件夹复制到 **dist/RunSpider/** 目录下 
    - 双击运行 **dist/RunSpider/RunSpider.exe**



### 六、演示Demo
![image](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzRiYTFjYzNjNTJiMGY3ZTRkZTUzNjMwNzY4MTYyYTdiYWEzOGZlYSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/2H8Q13nR71cFkD9r3q/giphy.gif)




### 七、遇到的问题
#### 1、使用selenium的ActionChains类实现滑块验证登录问题
- 虚拟鼠标：ActionChains类对鼠标的一系列点击移动操作都是**建立在虚拟鼠标**上的，电脑屏幕上实际看到的鼠标不会移动。
- 滑块移动轨迹问题：使用ActionChains需要自己生成滑块移动的轨迹方程，但是京东将大部分机器模拟的轨迹方程给禁止了导致正确移动到缺口位置也无法通过验证。**使用pyautogui控制滑块移动的轨迹更贴合人工操作。**
#### 2、使用pyautogui控制鼠标的坐标问题
- selenium能够直接获取网页元素然后进行操作，pyautogui必需通过获取要操作元素的坐标才能对元素进行操作。
- selenium中也能获取元素的坐标，但是该坐标是相对于**整个网页的左上角**的坐标。而pyautogui中要使用的元素的坐标是相对于**整个电脑屏幕左上角**的坐标。所以两者要进行一次转换。
#### 3、自动登录京东会遇到手机验证码
- 通过账号密码登录即使通过滑块验证也需要获取手机验证码。京东手机验证码的cookie有效时间是一个月，所以每隔一个月运行脚本时要重新获取一次手机验证码








