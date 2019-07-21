# -*- coding: UTF-8 -*-
# 包：py2-ipaddress==3.4.1
import ipaddress
a = ipaddress.IPv4Address('10.18.48.1')
b = ipaddress.IPv4Network('10.18.55.255')
print(a in b)
# ip地址a，在b网段中

