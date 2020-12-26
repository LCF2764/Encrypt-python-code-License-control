# Encrypt-python-code-License-control
python代码加密以及python代码的License控制

本工程适用于，码农给别人开发项目的时候，防止别人拿到代码后未经授权随意复制代码到未经权授的机器上运行，同时还将代码加密防止别人窃取核心机密。


## Overview
- python代码加密：将python代码编译成c/c++，然后再编译成python的扩展模块，即`.os`文件，起到保护python代码的目的，防止别修改/查看你的Python源码。
- License控制：为你的Python代码指定运行的主机，即只有获得你授权的计算机才能运行你的python代码，同时也可以为python代码设置有效期，过期后无法运行。


## Requirement

本工程能在**Linux系统python2环境**下顺利运行，其他环境可能会报错。

linux需安装：
- python-dev
- gcc

  ```
  sudo apt-get install python-dev gcc
  ```
  
python2需安装的第三方库：

- `pycrypto`（注意：在win10环境下安装这个包可能会报错，解决办法见[这里](<https://blog.csdn.net/woay2008/article/details/79905627>) ）

- `Cython`

  ```
  pip install pycrypto Cython
  ```
  
## Usage
TODO：将本工程下`Example/`目录下的代码加密并进行license控制

#### Step 0: Preparation
- 安装依赖包: `sudo apt-get install python-dev gcc`, `pip install Cython`
- 准备好你的加密秘钥和解密秘钥
密钥的格式参考`License_control/CreateLicense.py`里的`seperateKey`,`aesKey `,`aesIv`
- 准备好你待权授的计算机的MAC地址


#### Step 1: 加密python代码
将`Encrypt_py/get_time.py`加密
- 将待加密的python文件名填写到`Encrypt_py/setup.py`里的`key_funs`列表中。


- 加密脚本，运行
  ```
  cd Encrypt_py/
  python setup.py build_ext --inplace
  ```
程序运行成功的话会生成与`.py`文件同名的`.os`文件，加密完成。
将加密得到的`get_time.so`文件放到`/test`路径下：
```
cp get_time.so ../test
```


#### Step 2: 授权给用户主机
(即加密目标主机MAC地址)
- 获取目标主机的MAC地址
用`/License_control/GetHostInfo.py`这个脚本获取目标主机的MAC地址：

```
# 在目标主机执行以下程序, 会在控制台输出MAC地址
cd ../License_control
python GetHostInfo.py
```
- 指定`CreateLicense.py`中的密钥：`seperateKey`, `aesKey`,和 `aesIv`
- 加密MAC地址得到密文
cd到`License_control/`路径下，将上面得到的MAC地址填到`<MAC地址>`处
```

python CreateLicense.py <MAC地址>
```
生成licese.lic，此即为MAC的加密文件。将此密文放到`test/`路径下。
```
mv license.lic ../test
```


#### Step 3: 测试
```
cd ../test
python main.py
```

如过能成功执行，会显示如下信息：

```
2020-12-26 18:03:46.602125
hello world!
('The local time is now:', 'Sat Dec 26 18:03:46 2020')
```