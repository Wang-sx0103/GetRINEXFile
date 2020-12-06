import os
import time
from ftplib import FTP

with open("IGS Station Name.txt","r",encoding = "utf-8") as file:
    all_station_name = file.readlines()                                        #逐行读取站名
file1 = open("异常记录.txt","a",encoding= "utf-8")                             #建立异常记录文件
start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))    #开始时间
file1.write("执行时间："+start_time+"\n")

flag = True
while flag:
    Year = input("输入年份：")
    if int(Year) >= 1992 and int(Year) <= 2020:
        print("年份正常!")
        break
    else:
        print("年份错误,重新输入!")

while flag:
    Day = input("输入天数：")
    if int(Day) >= 1 and int(Day) <= 366:
        print("日期正常!")
        if int(Day)>=1 and int(Day) <= 9:
            Day = "00"+Day
        elif int(Day)>=10 and int(Day) <= 99:
            Day = "0"+Day
        break
    else:
        print("日期错误!")
#print("文件开始下载...")

#登入函数
def ftpconnect():

    ftp_server = 'igs.bkg.bund.de'#'cddis.nasa.gov'
    username = ''
    password = ''
    ftp=FTP()                                                                  #调用构造函数，生成对象
    #ftp.set_debuglevel(2)                                                     #打开调试级别2，显示详细信息
    print("正在连接服务器...")
    ftp.connect(ftp_server,21)                                                 #连接服务器
    print("正在登入服务器...")
    ftp.login(username,password)                                               #登录，空串代替匿名登入
    return ftp

def downloadfile():

    ftp = ftpconnect()
    print("文件开始下载")
    datapath1 = "/IGS/obs"#"/gnss/data/daily"
    for i in range(len(all_station_name)):
        try:
            station_name = all_station_name[i][0:-1]
            filename = station_name + "_R_" + Year + Day + "0000_01D_30S_MO.crx.gz"   #生成文件名称
            print(filename + "文件正在下载...")
            path = datapath1 + "/"+Year+ "/" + Day + "/" + filename #+Year[2:]+"d/"+ filename     #生成文件地址
            bufsize = 5120                                                            #设置缓冲块大小
            if os.path.exists(filename):
                print(filename+"已经存在！")
                continue
            else:
                fp = open(filename,'wb')                                              #以写模式在本地打开文件
                ftp.retrbinary("RETR " + path,fp.write,bufsize)                       #接收服务器上文件并写入本地文件
                fp.close()                                                                #文件关闭，释放使用权
                print(filename + "文件下载完成！")
        except Exception as ex_results:                                               #异常抓取
            if str(ex_results) == "550 Failed to open file.":                         #文件不存在异常
                file1.write(station_name+"文件不存在！"+"\n")
                print(filename + "文件不存在！") 
                fp.close()
                os.remove(filename)                                                   #删除空文件
            else:
                file1.write("抓到一个未处理异常："+str(ex_results)+"\n")
                print("抓到一个未处理异常：",ex_results)
    #ftp.set_debuglevel(0)                                                            #关闭调试
    ftp.quit()                                                                        #退出ftp服务器

if __name__=="__main__":

    downloadfile()
    print("所有文件下载完成!")
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    file1.write("结束时间："+ end_time+"\n")
    file1.close()
