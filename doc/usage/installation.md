# 安装方法

## 1. 安装Python > 2.7 （推荐使用 Python3，对 Python2.7 的支持有限，并且可能随时停止支持）

1. 如果已经安装 Python 请跳过该步骤，确保 python, pip 已在 PATH环境变量中

2. Linux 操作系统请自行安装 Python > 2.7

3. Windows 下载 Python3

    - [点击下载 Python 3.6.4 Windows x64](https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe)

    - [点击下载 Python 3.6.4 Windows x86](https://www.python.org/ftp/python/3.6.4/python-3.6.4.exe)

    - 提示：如果不知道系统类型请选择下载 Windows x86

4. 安装Python3

    - 右键点击安装程序，选择以管理员方式运行程序

    <div  align="center">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/windows_install_python/01.jpg?raw=True" width = "350" />
    </div>

    - 选择 **Customize Installation(自定义安装)**

    <div  align="center">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/windows_install_python/02.jpg?raw=True" width = "600" />
    </div>

    - 勾选所有选项，点击 **Next(下一步)**

    <div  align="center">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/windows_install_python/03.jpg?raw=True" width = "600" />
    </div>

    - 勾选 **Install for all users** 和 **Add Python to environment vaiables**, 选择好安装路径，点击 **Install(安装)**

    <div  align="center">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/windows_install_python/04.jpg?raw=True" width = "600" />
    </div>

    - 等待安装

    <div  align="center">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/windows_install_python/05.jpg?raw=True" width = "600" />
    </div>

    - 安装完成，点击 **Close(关闭)** 关闭安装程序

    <div  align="center">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/windows_install_python/06.jpg?raw=True" width = "600" />
    </div>

## 2. 下载和启动Words程序

1. 下载最新版 Words程序 [点击下载Words程序 latest.zip](https://github.com/StevenKjp/words/raw/master/build/latest.zip)

2. 运行Words服务器

    - 解压 latest.zip 到任何目录

    <div  align="center">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/run_server/01.jpg?raw=True" width = "200">
    </div>

    - 进入 **build_x.x.x** 文件夹 (其中 **x.x.x** 为最新版本号，随着程序更新会产生变化)

    <div  align="center">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/run_server/02.jpg?raw=True" width = "90">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/run_server/03.jpg?raw=True" width = "500">
    </div>

    - 确保计算机已联网 右键 start.cmd 以管理员方式运行

    <div  align="center">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/run_server/04.jpg?raw=True" width = "200">
    </div>

    - 等待服务启动, 直到出现 **Quit the server with CTRL-BREAK.**

     <div  align="center">
        <img src="https://github.com/StevenKjp/words/blob/master/doc/images/run_server/05.jpg?raw=True" width = "600">
    </div>

    **程序使用过程中，请不要关闭控制台窗口（控制台窗口就是上面那个黑框，如已关闭，请重新打开）**

    **程序使用过程中，请不要重复打开start.cmd**

    - Linux 操作系统请直接执行

        - sudo pip install -r requirements.txt --upgrade
        - python viewer/starter.py
