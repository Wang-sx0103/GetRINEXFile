# 解压gz文件函数
import os
import gzip


def init():
    global relativePath
    relativePath = "./resources"
    allFile = os.listdir(relativePath)
    for i in range(len(allFile)):
        # 只通过文件
        if os.path.isfile(relativePath+"/"+allFile[i]):
            # 只处理.gz文件
            if (allFile[i].split(".")[-1] == "gz"):
                gzName = allFile[i]
                unzip(gzName)


def unzip(filename):
    # 提取出年份
    year = filename.split("_")[2][2:4]
    # 获取文件的名称，并转换为D文件（.gz->.D）
    if filename.split(".")[-2] == "crx":
        unzipFile = filename.replace("crx.gz", year + "D")
    elif filename.split(".")[-2] == "rnx":
        unzipFile = filename.replace(".gz", "")
    # 创建gzip对象
    gzFile = gzip.GzipFile(relativePath+"/"+filename)
    # gzip对象用read()打开后，写入open()建立的文件里
    open(relativePath+"/"+unzipFile, "wb+").write(gzFile.read())
    # 关闭gzip对象
    gzFile.close()


if __name__ == "__main__":
    print("gz文件开始解压......")
    init()
    print("gz文件解压完成！")
