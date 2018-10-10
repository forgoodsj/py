#!/user/bin/env python
#coding=utf-8
import requests
import random
import json
url = 'https://jijinbaapi.eastmoney.com/gubaapi/v3/write/Article/Like/LikeReply.ashx'
url2 = 'https://jijinbaapi.eastmoney.com/gubaapi/v3/write/Article/Like/CancelLikeReply.ashx'

form = {
    'ServerVersion':'1.0.0',
    'PhoneType':'android',
    'Location':'zh-CN',
    'RandomNum':random.random()/100,
     'ctoken':'BSUaj9F6gdvdtGbG8f4NBSh0PmaeNHBsS541VfyvjQLwX3hLef-zEPoSqteaYtAr1PKLnLxV8ZtVXDMJUJChc1sVYzAOG_yTCCHr5MogL0LTIfp6iQdyHj6aiV39T-sHvIHtOJsZDQUgw6wIWgoJrn1K2liTLiSxRVZ20o4Jlyg',
    'utoken':'FobyicMgeV5n3saZh_euZ-tzp_rvpcbHETiJJyU5cvwJUqjNxV7KDQi09s18stejUTidv_q4Q5W9Ms6CTBQ3c64uUD-0TwGM8HPkCoxSl3XMO2ogpmDfvmr2Wn4IzNTi2CskzH-xUmxk5z9Au3CIgdFxj7Hd61NKjZU-kI77SF9BqCB5F45vxRJyWQC_gFjlRQ16yohk5MOeq3-7o0Em2k9lgavyYIGrgu1zRWSMBY-8Fs6qVVo-W8Z6jxasoG9x4HB6wAKw2BsSlTGE46-oC0xMl_lizbH1',
    'deviceId':'837EC5754F503CFAAEE0929FD48974E7',
    'userId':'',
    'plat':'Wap',
    'product':'Fund',
    'version':'201',
    'replyid':'8732034612',
    'postid':'784720163',
}

headers = {
    'Accept':'application/json',
    'Connection':'keep-alive',
    'Content-Length':'676',
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'jijinbaapi.eastmoney.com',
    'Origin':'https://fundbarmob.eastmoney.com',
    'Referer':'https://fundbarmob.eastmoney.com/',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
}

#requests.post(url,data=form, headers = headers)
response = requests.post(url,data=form,headers=headers)
if response.status_code == 200:
    print(response.json())
else:
    print(requests.ConnectionError())
