# -*- coding: UTF-8 -*-
import random
from typing import Any, Dict

from requests import post, get
from loguru import logger

_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9," +
              "image/avif,image/webp,image/apng,*/*;q=0.8,application/sig" +
              "ned-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Host": "192.168.1.1",
    "Origin": "http://192.168.1.1",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


def get_sysauth_cookie_value(username, psd) -> str:
    _h1 = _headers.copy()
    _h1['Content-Type'] = 'application/x-www-form-urlencoded'
    _h1["Referer"] = "http://192.168.1.1/cgi-bin/luci"
    resp = post(
        "http://192.168.1.1/cgi-bin/luci",
        headers=_h1,
        data=f'username={username}&psd={psd}',
        allow_redirects=False
    )
    if resp.status_code != 302:
        logger.error(f"""
        Maybe login failed .
        
        Code :
        {resp.status_code}
        
        Header :
        {resp.headers}
        
        Body:
        {resp.text}
        """)
        raise Exception(f"Except 302 , but {resp} , maybe login failed .")
    return resp.cookies.get('sysauth')


def get_gwinfo(*, sysauth_cookie) -> Dict[str, Any]:
    _h1 = _headers.copy()
    _h1['Referer'] = 'http://192.168.1.1/cgi-bin/luci/admin/settings/info'
    _h1['Cookie'] = f'sysauth={sysauth_cookie}'
    resp = get('http://192.168.1.1/cgi-bin/luci/admin/settings/gwinfo',
               headers=_h1,
               params={
                   'get': 'part',
                   '_': random.uniform(0, 1)
               })
    logger.info(f"gwinfo response body : {resp.text}")
    return resp.json()


def get_pub_ip(*, sysauth_cookie):
    return get_gwinfo(sysauth_cookie=sysauth_cookie)['WANIP']


if __name__ == '__main__':
    pass
