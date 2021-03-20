# -*- coding: utf-8 -*-
# igs.ign.fr/pub/igs/data/campaign/mgex/daily/rinex3/
import os
import time
from ftplib import FTP


'''
init():
    初始化程序所需要的必要变量
    建立异常记录文件：exceptionFile
    逐行读取站名至列表：allStationName
    获取日期
'''


def init():
    with open("IGSStationName.txt", "r", encoding="utf-8") as file:
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
    # 获取年和天数
    global year
    year = eval(input("输入年份："))
    global startDay
    startDay = eval(input("输入开始天数："))
    global endDay
    endDay = eval(input("输入结束天数："))


'''
ftpConnect():
    连接并登入服务器
'''


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
    ftp.getwelcome()
    # 登录，空串代替匿名登入
    ftp.login(username, password)
    return ftp


'''
downloadFile()函数：

'''


def downloadFile():
    global ftp
    global fp
    global fileSize
    global downloadSize
    downloadSize = 0
    ftp = ftpConnect()
    # "/IGS/obs"/"/gnss/data/daily"
    datapath1 = "pub/igs/data/campaign/mgex/daily/rinex3/"
    constant1 = "_R_"
    constant2 = "0000_01D_30S_MO.crx.gz"
    constant3 = "0000_01D_CN.rnx.gz"

    for i in range(len(allStationName)):
        for Day in range(startDay, endDay+1):
            try:
                stationName = allStationName[i][0:]
                # 生成文件名称
                observationFile = stationName + constant1 + str(year) + \
                    date2Str(Day) + constant2
                navigationFile = stationName + constant1 + str(year) + \
                    date2Str(Day) + constant3

                # Observation文件下载
                if os.path.exists("./resources/" + observationFile):
                    print(observationFile + "已经存在！")
                else:
                    print(observationFile + "文件开始下载...")
                    serverPath = datapath1 + str(year) + \
                        "/" + date2Str(Day) + "/" + observationFile
                    if os.path.exists("./resources"):
                        fp = open("./resources/" + observationFile, 'wb')
                    else:
                        os.mkdir("resources")
                        fp = open("./resources/" + observationFile, 'wb')
                    fileSize = ftp.size(serverPath)
                    # 接收服务器上文件并写入本地文件
                    ftp.retrbinary(
                        cmd="RETR " + serverPath,
                        callback=downloadBar,
                        blocksize=81920)
                    # 重置文件的大小
                    downloadSize = 0
                    print()
                    # 文件关闭，释放使用权
                    fp.close()
                    print(observationFile + "文件下载完成！")
                    print(
                        "文件大小：" +
                        str(formatSize(fileSize)[0]) +
                        formatSize(fileSize)[1])
                    print("----"*20)

                # Navigation文件下载
                if os.path.exists("./resources/" + navigationFile):
                    print(navigationFile + "已经存在！")
                else:
                    print(navigationFile + "文件开始下载...")
                    serverPath = datapath1 + str(year) + \
                        "/" + date2Str(Day) + "/" + navigationFile
                    if os.path.exists("./resources"):
                        fp = open("./resources/" + navigationFile, 'wb')
                    else:
                        os.mkdir("resources")
                        fp = open("./resources/" + navigationFile, 'wb')
                    fileSize = ftp.size(serverPath)
                    # 接收服务器上文件并写入本地文件
                    ftp.retrbinary(
                        cmd="RETR " + serverPath,
                        callback=downloadBar,
                        blocksize=81920)
                    # 重置文件的大小
                    downloadSize = 0
                    print()
                    # 文件关闭，释放使用权
                    fp.close()
                    print(navigationFile + "文件下载完成！")
                    print(
                        "文件大小：" +
                        str(formatSize(fileSize)[0]) +
                        formatSize(fileSize)[1])
                    print("----"*20)

            except Exception as ex_results:
                if str(ex_results) == "550 Failed to open file.":
                    exceptionFile.write(observationFile + "文件不存在！" + "\n")
                    print(observationFile + "文件不存在！")
                    fp.close()
                    # 删除空文件
                    os.remove(observationFile)
                else:
                    exceptionFile.write("抓到一个未处理异常：" + str(ex_results) + "\n")
                    print("抓到一个未处理异常：", ex_results)
    # 退出ftp服务器
    ftp.quit()


'''
date2Str(day)函数：
    day：这一年的第几天
    return：字符串类型的天数（012、001、123）
'''


def date2Str(day):
    if 0 <= day <= 9:
        return "00" + str(day)
    elif 10 <= day <= 99:
        return "0"+str(day)
    else:
        return str(day)


'''
getFileSize(fileSize):
    fileSize：服务器端文件大小
    return：规范文件的单位
'''


def formatSize(fileSize):
    if 0 < fileSize <= 1024:
        return (fileSize, "B")
    else:
        fileSize = fileSize/1024
        if 0 < fileSize <= 1024:
            return (round(fileSize, 2), "KB")
        else:
            fileSize = fileSize/1024
            if 0 < fileSize <= 1024:
                return (round(fileSize, 2), "MB")
            else:
                fileSize = fileSize/1024
                return (round(fileSize, 2), "GB")


'''
downloadBar(block):
    此为回调函数
    block：获取正在下载的文件某次获得的数据大小
    downloadSize：总已下载大小
    fileSize：带下载文件在服务器中的大小
'''


def downloadBar(block):
    global downloadSize
    global fileSize
    fp.write(block)
    downloadSize = downloadSize + len(block)
    print("\r下载进度：{:.2%}".format(downloadSize/fileSize), end="")


'''
懂得都懂
'''


if __name__ == "__main__":
    init()
    downloadFile()
    print("所有文件下载完成!")
    print("\a")
    exceptionFile.write(
        "结束时间：" +
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) +
        "\n")
    exceptionFile.close()
