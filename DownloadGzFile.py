# -*- coding: utf-8 -*-
import os
import time
from ftplib import FTP

# 加载初始化


def init():
    with open("IGS Station Name.txt", "r", encoding="utf-8") as file:
        # 逐行读取站名
        global allStationName
        allStationName = file.readlines()
    # 建立异常记录文件
    global exceptionFile
    exceptionFile = open("异常记录.txt", "a", encoding="utf-8")
    # 记录异常开始时间
    recordStart = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime(time.time()))
    exceptionFile.write("执行时间：" + recordStart + "\n")
    # 获取
    global year
    year = eval(input("输入年份："))
    global startDay
    startDay = eval(input("输入开始天数："))
    global endDay
    endDay = eval(input("输入结束天数："))


def ftpConnect():
    # 'igs.bkg.bund.de'/'cddis.nasa.gov'
    ftp_server = 'igs.ign.fr'
    username = ''
    password = ''
    # 调用构造函数，生成对象ftp
    ftp = FTP()
    # ftp.set_debuglevel(2)#打开调试级别2，显示详细信息
    print("正在连接服务器...")
    # 连接服务器
    ftp.connect(ftp_server, 21)
    print("正在登入服务器...")
    # 登录，空串代替匿名登入
    ftp.login(username, password)
    return ftp


def downloadfile():
    ftp = ftpConnect()
    print("文件开始下载")
    # "/IGS/obs"/"/gnss/data/daily"
    datapath1 = "pub/igs/data/campaign/mgex/daily/rinex3/"
    constant1 = "_R_"
    constant2 = "0000_01D_30S_MO.crx.gz"
    for i in range(len(allStationName)):
        for Day in range(startDay, endDay+1):
            try:
                stationName = allStationName[i][0:]
                # 生成文件名称
                fileName = stationName + constant1 + year + Day + constant2
                if os.path.exists(fileName):
                    print(fileName+"已经存在！")
                    continue
                print(fileName + "文件开始下载...")
                path = datapath1 + year + "/" + Day + "/" + fileName
                # 设置缓冲块大小
                bufsize = 5120
                fp = open(fileName, 'wb')
                # 接收服务器上文件并写入本地文件
                ftp.retrbinary("RETR " + path, fp.write, bufsize)
                # 文件关闭，释放使用权
                fp.close()
                print(fileName + "文件下载完成！")
            except Exception as ex_results:
                if str(ex_results) == "550 Failed to open file.":
                    exceptionFile.write(fileName + "文件不存在！" + "\n")
                    print(fileName + "文件不存在！")
                    fp.close()
                    # 删除空文件
                    os.remove(fileName)
                    exceptionFile.write("抓到一个未处理异常：" + str(ex_results) + "\n")
                    print("抓到一个未处理异常：", ex_results)
    # 退出ftp服务器
    ftp.quit()


if __name__ == "__main__":
    init()
    downloadfile()
    print("所有文件下载完成!")
    endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    exceptionFile.write("结束时间：" + endTime + "\n")
    exceptionFile.close()
