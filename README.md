# 介绍
XX移动用于定期检测公网端口开放状态的工具。

## 效果
[](https://github.com/SRW-OG/chinamobileportdiscover/blob/master/Pics/snipaste20190228_111808.png)

# 环境
CentOS 7.5
python36

# 安装
1. 安装`nmap`
```
yum install nmap
```

2. 安装`python36`
```
yum install epel-release

yum install python36

curl -O https://bootstrap.pypa.io/get-pip.py
python36 get-pip.py

```

3. 安装程序依赖，在程序目录下
```
pip3 install -r requirements.txt
```

4. 运行
```
python36 run.py
```

5. 计划任务



# 注意
- 程序全部使用了绝对路径，需要修改的话统一进行修改
- docs目录下的基准文件命名固定，创建相关文件的md5的空文件
