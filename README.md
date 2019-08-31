# Encrypt-python-code-License-control
python代码加密以及python代码的License控制
# Overview
- python代码加密：将python代码编译成c/c++，然后再编译成python的扩展模块，即`.os`文件，起到保护python代码的目的，防止别修改/查看你的Python源码。
- License控制：为你的Python代码指定运行的主机，即只有获得你授权的计算机才能运行你的python代码，同时也可以为python代码设置有效期，过期后无法运行。

# Requirement
- Python: 2.7 (Update to 3.6/3.7 should be easy.)
- Linux （暂时不支持windows系统）
- pycrypto
# Usage
示例：现在要交付代码给用户，但是想限定用户只能在经你权授的计算机上执行这些代码。根据以下步骤即可实现这个功能。

- ##  encypt python code
### Step 0: Preparation
- 安装依赖包: 
- 准备好你的加密秘钥和解密秘钥
- 准备好你想权授的计算机的MAC地址

### step 1: 参考`hello.py`修改你的代码
- 将代码的核心部分封装成库(类或函数)，并保存为单独的py文件，以便于加密。
- 主函数部分可以暴露给客户不需要加密，只需把调用的函数进行加密

### step 2: encrypt python code
- 修改setup.py中的变量`key_funs`中的元素为你需要加密的`.py`文件名，可同时操作多个文件。请备份py文件，加密后会删除原文件。
- cd 到当前工作路径(setup.py所在的路径)，运行
```
python setup.py build_ext --inplace
```
程序运行成功的话会生成与`.py`文件同名的`.os`文件，这就是加密了的`.py'文件

- ## License control
### step 0: 授权给目标主机
(即加密目标主机MAC地址)
- 获取目标主机的MAC地址
- 指定`CreateLicense.py`中的密钥：`seperateKey`, `aesKey`,和 `aesIv`
- 在命令行中运行
```linux
python CreateLicense.py <MAC地址>
```
生成licese.lic，此即为MAC的加密文件

### step 1: 将加密文件传给客户
- 客户拿到`license.lic`文件后放在工程目录下
- 程序检测到`license.lic`文件后会解密出你加密的MAC地址，并与当前运行程序的计算机的MAC地址进行匹配，如果匹配成功则进入主程序正常实现代码的功能，如果匹配失败则退出程序。

