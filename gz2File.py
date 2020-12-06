import os 
import gzip 

#解压gz文件函数
def uncompress_gz(filename):
    year = filename.split("_")[2][2:4]                           #提取出年份
    f_name = filename.replace(".gz","."+ year+"D")               #获取文件的名称，并转换为D文件
    g_file = gzip.GzipFile(filename)                             #创建gzip对象
    open(f_name, "wb+").write(g_file.read())                     #gzip对象用read()打开后，写入open()建立的文件里。
    g_file.close()                                               #关闭gzip对象

file_list = os.listdir()                                          #获取当前目录下的所有文件和子目录

for i in range(len(file_list)):
    
    if os.path.isfile(file_list[i]):                              #只通过文件
        
        if file_list[i].split(".")[-1] == "gz":
            gzname = file_list[i]
            uncompress_gz(gzname)

print("gz文件解压完成！")
print("D文件向O文件转换...")
os.system("批量转换")
print("转换完成")