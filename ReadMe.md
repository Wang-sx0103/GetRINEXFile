[TOC]

### 获取crx文件和rnx文件  ###
- 0 运行DownloadGzFile.py文件
- 1 基本过程
	- 读取本地文件“IGSStationName.txt”，获取待下在站名
	- 与用户交互，获取下载待文件的年份及该年的起止天数
	- 通过FTP协议匿名登录服务器“igs.ign.fr”
	- 文件下载，包含两类文件：导航文件和观测文件。其中导航文件为混编文件各导航卫星都有包括，以30秒为一个历元；观测文件只有北斗卫星导航系统。

### 解压文件并转换 ###
- 0 运行gz2rnx.py文件
- 1 对rnx文件(xxxx...xxxx_01D_CN.rnx.gz)的操作
	- 该文件无需转换解压完即为所需要的导航文件（.rnx）
- 2 crx文件(xxxx...xxxxx_01D_30S_MO.crx.gz)的操作
	- 解压文件并修改文件类型为.yyD
	- 运行“批量转换.bat”获得观测文件(.yyO)
		该文件需要与crx2rnx.exe文件一同在.yyD文件下

### 注意事项 ###
- 每次下载会检查./resources文件夹里是否已存在相应文件
- 建立异常记录（异常记录.txt）文件，~~自己不会用而导致出错~~
- 符号含义
	- M:MIX
	- D:DAY
	- y:YEAR(only 2 numbers)
	- S:SECOND
	- RINEX文件详细信息:  [RINEX3.05](https://files.igs.org/pub/data/format/rinex305.pdf "RINEX305")
- python解释器版本不低于3.0

### Feedback ###
- 1 email:AnonymityA@qq.com