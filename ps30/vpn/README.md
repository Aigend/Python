sh upload.sh PS-NIO-3285ff15-7f564f27 ~/1.jpg
sh download.sh PS-NIO-3285ff15-7f564f27 1.jpg




# OpenVpn NAT 反向连接工具

在使用NAT的方案时，我们无法从内网直接访问vpn连接客户端的虚拟ip。 因此，我们需要一种特殊方式，来进行反向访问

## 原理

- 在每台openvn服务器上采集在线的openvpn信息
- 我们在每台openvpn 开启一个http代理服务
- 通过api，查询特定证书的证书名称，找到对应的虚拟地址，以及这台openvpn server的地址, 并把这个openvpn server的地址作为http的代理地址，去访问对应的虚拟地址

### API

通过http://ENPOINT URL/docs 访问api文档

### 客户端工具

我提供了一个反向ssh的客户端工具， 目前只适配了mac 和linux平台

### 使用

下载corkscrew， https://github.com/bryanpkc/corkscrew.git， 并放到/usr/local/bin/corkscrew

写一个配置文件，`vpnapi.ini`

```ini
[api]
url=http://10.138.120.71:8000
user=USER
password=PASSWORD
```

#### 列出所有的在线客户端
    python3 vpn_jump.py -c example_vpnapi.ini list

#### 连接某个证书所在的vpn服务器

    python3 vpn_jump.py -c example_vpnapi.ini ssh VpnBrownDragon_test_cert

#### 上传文件/tmp/abc到某个证书所在vpn服务器的家目录

    python3 vpn_jump.py -c example_vpnapi.ini scp upload VpnBrownDragon_test_cert /tmp/abc

#### 下载服务器上的/tmp/abc到当前目录

    python3 vpn_jump.py -c example_vpnapi.ini scp download VpnBrownDragon_test_cert /tmp/abc

#### 对某个证书添加描述

    python3 vpn_jump.py -c example_vpnapi.ini tag VpnBrownDragon_test_cert -t 欧洲测试证书

