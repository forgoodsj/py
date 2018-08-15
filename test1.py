#!/user/bin/env python
#coding=utf-8
u = '\\u7f51\\u7edc\\u4e0d\\u7ed9\\u529b\\uff0c\\u8bf7\\u7a0d\\u540e\\u91cd\\u8bd5!'
u1 ='\\U7f51\\U7edc\\U4e0d\\U7ed9\\U529b\\Uff0c\\U8bf7\\U7a0d\\U540e\\U91cd\\U8bd5!'
u2 = u.encode('utf-8').decode('unicode-escape')
print(u2)