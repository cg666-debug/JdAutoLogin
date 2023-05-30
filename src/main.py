import schedule
import time
import sys
import os
import subprocess
# 定义你要周期运行的函数
def job():
    """
    利用subprocess执行命令行运行RunSpider.py
    """
    #获取当前代码执行的路径
    DIR = sys.path[0]
    #获取执行爬虫代码的命令行    
    RunSpiderCommandLine = "python "+DIR+"\RunSpider.py"
    print(RunSpiderCommandLine)
    subprocess.call(RunSpiderCommandLine,shell=True)

"""
在这可以设置自己想要运行的时间

以下是一些例子

注意京东的手机验证码cookie的时效是一个月
"""
#schedule.every(10).minutes.do(job)               # 每隔 10 分钟运行一次 job 函数
#schedule.every().hour.do(job)                    # 每隔 1 小时运行一次 job 函数
schedule.every().day.at("19:21").do(job)         # 每天在 10:30 时间点运行 job 函数
#schedule.every().monday.do(job)                  # 每周一 运行一次 job 函数
#schedule.every().wednesday.at("13:15").do(job)   # 每周三 13：15 时间点运行 job 函数
#schedule.every().minute.at(":17").do(job)        # 每分钟的 17 秒时间点运行 job 函数

#job()
while True:
    schedule.run_pending()   # 运行所有可以运行的任务
    time.sleep(10)
    
"""
注意关闭main.py得终止该进程。关闭京东页面只是终止了爬虫进程,上述循环判断还在进行中
"""
